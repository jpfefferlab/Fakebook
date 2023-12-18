from django.urls import re_path

import chat.consumers
import analytics.consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_slug>\d+-\d+)/$', chat.consumers.ChatWebSocketConsumer.as_asgi()),
    re_path(r'ws/analytics/$', analytics.consumers.AnalyticsWebSocketConsumer.as_asgi()),
]