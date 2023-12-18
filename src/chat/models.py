from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile
from django.db.models.deletion import CASCADE

class Chat(models.Model):
    slug = models.SlugField(unique=True)
    user_1 = models.ForeignKey(Profile, on_delete=CASCADE, related_name='user_1')
    user_2 = models.ForeignKey(Profile, on_delete=CASCADE, related_name='user_2')

    def users(self):
        return [self.user_1, self.user_2]

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=CASCADE)
    user = models.ForeignKey(Profile, on_delete=CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date',)