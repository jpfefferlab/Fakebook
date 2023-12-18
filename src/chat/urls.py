from django.urls import path
from .views import start_chat, chat_drawer

app_name = 'chats'

urlpatterns = [
    path('', start_chat, name='start-chat'),
    path('drawer', chat_drawer, name='chat-drawer'),
]