import random
import string

from django.db import models

class Configuration(models.Model):
    chat_enabled = models.BooleanField(default=True)
    chat_friends_only = models.BooleanField(default=False)
    posts_friends_only = models.BooleanField(default=False)
    comments_friends_only = models.BooleanField(default=False)
    profiles_friends_only = models.BooleanField(default=False)
    comments_enabled = models.BooleanField(default=True)
    relationship_management_enabled = models.BooleanField(default=True)
    registration_enabled = models.BooleanField(default=True)
    management_token = models.CharField(default="changeme", max_length=100)

    def regenerate_mgmt_token(self):
        self.management_token = "".join([random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(16)])
        self.save()


def get_the_config() -> Configuration:
    config = Configuration.objects.first()
    if config is None:
        print("Config not found! Creating config...")
        config = Configuration.objects.create()
    if config.management_token == "changeme":
        config.regenerate_mgmt_token()
    return config

def ensure_config_exists():
    c = get_the_config()
    if not c:
        raise RuntimeError("Could not create configuration")