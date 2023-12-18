import re
import json
from json.decoder import JSONDecodeError
from typing import List

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from django.contrib.auth.models import User

from configuration.models import get_the_config
from profiles.models import Profile
from chat.models import Chat, Message

CHAT_WEBSOCKET_PATH_PATTERN = r"/ws/chat/(\d+)-(\d+)"

def get_chat_user_ids_from_path(path):
    matcher = re.compile(CHAT_WEBSOCKET_PATH_PATTERN)
    match = matcher.match(path)

    return [int(match.group(1)), int(match.group(2))]


# Synchronous consumer -> can access models
class ChatWebSocketConsumer(WebsocketConsumer):

    own_user: User
    own_id: int
    own_profile: Profile
    profile_ids: List[int]
    other_id: int
    other_user: User
    other_profile: Profile
    chat: Chat

    def connect(self):
        # Check if chat enabled
        if not get_the_config().chat_enabled:
            self.close()
            raise PermissionError("Chat disabled, aborting connection")

        self.own_user = self.scope["user"]
        self.own_profile = Profile.objects.get(user=self.own_user)
        self.own_id = self.own_profile.id

        self.profile_ids = get_chat_user_ids_from_path(self.scope["path"])

        if self.own_id not in self.profile_ids:
            self.close()
            raise PermissionError(f"User {self.own_user.username}({self.own_id}) tried to access chat {self.scope['path']} without being a member")

        self.other_id = [id for id in self.profile_ids if id != self.own_id][0]
        self.other_profile = Profile.objects.get(id=self.other_id)
        self.other_user = self.other_profile.user

        if not self.other_profile:
            self.close()
            raise KeyError(f"User for id {self.other_id} not found")

        if len(self.profile_ids) != 2 or self.profile_ids[0] == self.profile_ids[1]:
            self.close()
            raise RuntimeError(f"Invalid chat parameters, user_ids: {self.profile_ids}")

        # Check if friend
        if get_the_config().chat_friends_only and self.other_profile.user not in self.own_profile.friends.all():
            self.close()
            raise RuntimeError(f"User {self.own_user.username} attempted to chat with non friend {self.other_user.username}, aborting...")

        # Create chat
        if self.own_id < self.other_id:
            self.chat, created = Chat.objects.get_or_create(slug=f"{self.own_id}-{self.other_id}", user_1=self.own_profile, user_2=self.other_profile)
        else:
            self.chat, created = Chat.objects.get_or_create(slug=f"{self.other_id}-{self.own_id}", user_1=self.other_profile, user_2=self.own_profile)

        if created:
            self.chat.save()

        # Create and join group/channel
        async_to_sync(self.channel_layer.group_add)(
            self.chat.slug,
            self.channel_name
        )

        self.accept()

    def send_all_messages_to_client(self):
        all_messages = Message.objects.filter(chat=self.chat)
        all_messages_sorted = sorted(all_messages, key=lambda m: m.date)

        for message in all_messages_sorted:
            self.send_message_to_client(message)

    def send_message_to_client(self, message: Message):
        self.send(json.dumps({
            "type": "message",
            "content": message.content,
            "timestamp": round(message.date.timestamp()),
            "source_user_id": message.user.id,
            "own_message": message.user.id == self.own_id
        }))

    # called / received via channel
    def chat_message_notification(self, event):
        msg_id = event["id"]

        message = Message.objects.get(id=msg_id)

        if not message:
            raise RuntimeError("Couldn't find message")

        if message.chat != self.chat or not message.user.id in self.profile_ids:
            raise RuntimeError("Received a channels notification for a message not belonging to this chat")

        self.send_message_to_client(message)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        try:
            packet = json.loads(text_data)
        except JSONDecodeError:
            raise RuntimeError("Couldn't decode JSON of incoming chat message request")

        if packet["type"] == "request_all_messages":
            self.send_all_messages_to_client()
        elif packet["type"] == "send_message":
            message = Message.objects.create(chat=self.chat, user=self.own_profile, content=packet["content"])
            message.save()

            # Everyone in this group will receive the event, so both we and the other user will be notified (even on multiple sessions)

            async_to_sync(self.channel_layer.group_send)(
                self.chat.slug,
                {
                    "type": "chat_message_notification",
                    "id": message.id
                }
            )

        else:
            raise ValueError(f"Unknown chat packet type: {packet['type']}")

