from django.db import models

from profiles.models import Profile
from posts.models import Post

class TrackedSession(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="tracked_sessions")
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now_add=True)


class TrackedPostView(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="tracked_post_views")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="tracked_views")
    total_time_ms = models.BigIntegerField(default=0)