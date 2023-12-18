
from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile

from django.utils import timezone

from .utils import format_likes_string

class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    disliked = models.ManyToManyField(Profile, blank=True, related_name='dislikes')
    reported = models.ManyToManyField(Profile, blank=True, related_name='reports')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.content[:20])

    def num_likes(self):
        return self.liked.all().count()

    def num_dislikes(self):
        return self.disliked.all().count()

    def num_reports(self):
        return self.reported.all().count()

    def num_comments(self):
        return self.comment_set.all().count()

    def likers(self):
        return [profile.get_displayed_name() for profile in self.liked.all()]

    def dislikers(self):
        return [profile.get_displayed_name() for profile in self.disliked.all()]

    def likes_string(self):
        LIKES_TO_SHOW = 5
        return format_likes_string(self.likers(), LIKES_TO_SHOW)

    def dislikes_string(self):
        DISLIKES_TO_SHOW = 5
        return format_likes_string(self.dislikers(), DISLIKES_TO_SHOW)

    class Meta:
        ordering = ('-created',)

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    spoiler = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model): 
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"

DISLIKE_CHOICES = (
    ('Dislike', 'Dislike'),
    ('Undislike', 'Undislike'),
)

class Dislike(models.Model): 
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=DISLIKE_CHOICES, max_length=9)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"

REPORT_CHOICES = (
    ('Report', 'Report'),
    ('Unreport', 'Unreport'),
)

class Report(models.Model): 
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=REPORT_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"

PLANNED_REACTION_CHOICES = (
    ('Like', 'Like'),
    ('Dislike', 'Dislike')
)

class PlannedReaction(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    time_delta = models.IntegerField(default=0)
    reaction_type = models.CharField(choices=PLANNED_REACTION_CHOICES, max_length=8)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)

    target_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, related_name="target_profile")
    post_offset = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return f"{self.user}-{self.time_delta}-{self.reaction_type}--{self.post}--{self.target_profile}--{self.post_offset}"

