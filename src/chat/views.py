from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from configuration.models import get_the_config
from fakebook.settings import LAST_MESSAGE_CHAT_DRAWER_MAX_LENGTH
from profiles.models import Profile
from .models import Chat, Message
from django.http import HttpResponse

def get_slug(id1, id2) -> str:
    return "-".join([str(id) for id in sorted([id1, id2])])


@login_required
def start_chat(request):
    if request.method != 'GET':
        return

    user_1 = Profile.objects.get(user=request.user)
    user_1_id = user_1.id
    user_2_id = request.GET.get('profile_pk')
    user_2 = Profile.objects.get(pk=user_2_id)

    slug_string = get_slug(user_1_id, int(user_2_id))

    # chat, created = Chat.objects.get_or_create(slug=slug_string, user_1 = user_1, user_2 = user_2)
    #
    # if created:
    #     chat.save()

    ctx = {
        "own_id": user_1_id,
        "other_id": user_2_id,
        "own_avatar_image_url": user_1.avatar.url,
        "other_avatar_image_url": user_2.avatar.url,
        "other_username": user_2.get_displayed_name(),
        "slug": slug_string
    }

    # return HttpResponse(slug_string, content_type="text/plain")
    response = render(request, 'chat/chat.html', context=ctx)
    response['Content-Security-Policy'] = "frame-ancestors 'self'"  # allow embedding this on the own page as iframe
    return response

@login_required
def chat_drawer(request):
    if request.method != 'GET':
        return

    # abort early to avoid loading all users
    if not get_the_config().chat_enabled:
        ctx = {
            "users": [],
            "chat_enabled": False
        }
        response = render(request, 'chat/chat-drawer.html', context = ctx)
        response['Content-Security-Policy'] = "frame-ancestors 'self'"  # allow embedding this on the own page as iframe
        return response

    own_user = request.user
    own_profile = Profile.objects.get(user=request.user)

    users = []

    all_profiles = Profile.objects.get_all_profiles(me=own_user)

    # determine time of last chat
    last_message_by_profile = {}
    for profile in all_profiles:
        last_message_by_profile[profile] = {"msg": "", "timestamp": 0, "date": None}

        chat = Chat.objects.filter(slug=get_slug(own_profile.id, profile.id)).first()
        if not chat:
            continue

        messages = Message.objects.filter(chat=chat)
        if len(messages) == 0:
            continue

        last_message = max(messages, key=lambda m: m.date)
        if not last_message:
            continue

        last_message_content = last_message.content
        if len(last_message_content) > LAST_MESSAGE_CHAT_DRAWER_MAX_LENGTH:
            last_message_content = last_message.content[0:(LAST_MESSAGE_CHAT_DRAWER_MAX_LENGTH - 3)] + "..."

        last_message_by_profile[profile] = {"msg": last_message_content, "timestamp": last_message.date.timestamp(), "date": last_message.date}

    all_profiles_sorted = sorted(all_profiles, key=lambda p: last_message_by_profile[p]["timestamp"], reverse=True)

    # list non friends at the bottom or filter them completely
    friends = [p for p in all_profiles_sorted if (p.user in own_profile.friends.all())] # TODO use a filter DB query
    non_friends = [p for p in all_profiles_sorted if not p in friends]

    visible_profiles = []

    if get_the_config().chat_enabled:
        visible_profiles += friends

        if not get_the_config().chat_friends_only:
            visible_profiles += non_friends

    for profile in visible_profiles:
        users.append({
            "profile_id": profile.id,
            "username": profile.get_displayed_name(),
            "avatar_image": profile.avatar.url,
            "last_message": last_message_by_profile[profile]["msg"],
            "last_message_creation_time": last_message_by_profile[profile]["date"]
        })

    ctx = {
        "users": users,
        "chat_enabled": get_the_config().chat_enabled
    }

    response = render(request, 'chat/chat-drawer.html', context = ctx)
    response['Content-Security-Policy'] = "frame-ancestors 'self'"  # allow embedding this on the own page as iframe
    return response