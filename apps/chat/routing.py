from django.urls import re_path
from apps.chat.consumers import ChatConsumer

# Укажите путь для WebSocket
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]