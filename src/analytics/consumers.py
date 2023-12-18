import json
from datetime import datetime, timedelta

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from django.contrib.auth.models import User, AnonymousUser

from analytics.models import TrackedSession, TrackedPostView
from fakebook.settings import ANALYTICS_UPDATE_PERIOD_MS, ANALYTICS_SESSION_TIMEOUT_MS
from posts.models import Post
from profiles.models import Profile

class AnalyticsWebSocketConsumer(WebsocketConsumer):

    user: User
    profile: Profile
    tracked_session: TrackedSession

    def connect(self):
        self.user = self.scope["user"]

        if self.user is None or isinstance(self.user, AnonymousUser) or self.user.id is None:
            self.accept()
            self.send(json.dumps({
                "type": "status",
                "status": "unauthorized",
                "message": "You are not logged in."
            }))
            self.close()
            return

        self.profile = Profile.objects.get(user=self.user)

        if self.profile is None:
            self.close()
            raise ValueError(f"No profile found for user {self.user.username}, couldn't initialize analytics")

        # create and update session
        self.tracked_session = TrackedSession.objects.filter(profile=self.profile, last_seen__gte=(datetime.now() - timedelta(milliseconds=ANALYTICS_SESSION_TIMEOUT_MS))).order_by("-last_seen").first()

        if self.tracked_session is None:
            self.tracked_session = TrackedSession.objects.create(profile=self.profile)
            self.tracked_session.save()

        self.accept()

        self.send_config()

    def send_config(self):
        self.send(json.dumps({
            "type": "config",
            "updatePeriod": ANALYTICS_UPDATE_PERIOD_MS
        }))

    def receive(self, text_data=None, bytes_data=None):
        msg = json.loads(text_data)
        msg_type = msg["type"]

        if msg_type == "heartbeat":
            self.tracked_session.last_seen = datetime.now()
            self.tracked_session.save()

            # print(f"Heartbeat on -> Start: {self.tracked_session.first_seen}, Last seen: {self.tracked_session.last_seen}")

            # process viewed posts
            post_exposure_durations = msg["postExposures"]

            for exposure in post_exposure_durations:
                seen_post = Post.objects.get(id=exposure["postId"])

                if seen_post is None:
                    print(f"Couldn't find seen post {exposure['postId']} for analytics")
                    continue

                tracked_post_view, created = TrackedPostView.objects.get_or_create(profile=self.profile, post=seen_post)
                tracked_post_view.total_time_ms += exposure["duration"]
                tracked_post_view.save()

                # print(f"Seen post for {exposure['duration']}, total: {tracked_post_view.total_time_ms}: ", seen_post.content)

        pass

    def disconnect(self, close_code):
        pass