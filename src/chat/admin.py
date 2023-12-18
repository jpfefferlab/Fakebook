from django.contrib import admin
from .models import Chat, Message
from fakebook.downloads import get_csv

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ['id', 'user_1_id', 'user_2_id']

    def download_csv(self, request, queryset):
        response = get_csv(self.list_display, queryset, 'chats.csv')
        return response

    download_csv.short_description = "Download CSV file"

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ['source_user', 'target_user', 'content', 'date']

    def download_csv(self, request, queryset):
        response = get_csv(self.list_display, queryset, 'messages.csv')
        return response

    def source_user(self, msg):
        return msg.user.user.username

    def target_user(self, msg):
        return [p for p in msg.chat.users() if p != msg.user][0].user.username

    download_csv.short_description = "Download CSV file"