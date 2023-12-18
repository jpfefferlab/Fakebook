from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile


class Advertisement(models.Model):
    image = models.ImageField(upload_to='advertisements', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=False)
    text = models.TextField()
    url = models.URLField(max_length=200, default="")
    num_clicked = models.IntegerField(default=0)
    user_clicked = models.ManyToManyField(Profile, blank=True, related_name='clicked')
    #reported = models.ManyToManyField(Profile, blank=True, related_name='reported')

    def __str__(self):
        return f"{self.text}"
