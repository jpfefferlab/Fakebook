from django.contrib import admin

# Register your models here.
from configuration.models import Configuration


# unloading modules to hide them from the admin panel, this app is loaded AFTER allauth, so it can unregister
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from django.contrib import admin

admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(EmailAddress)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ["change_configuration", "chat_enabled", "chat_friends_only", "posts_friends_only", "comments_friends_only", "profiles_friends_only", "comments_enabled", "relationship_management_enabled", "registration_enabled", "management_token"]

    def change_configuration(self, configuration):
        return "change configuration"

