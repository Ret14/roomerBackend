
from django.urls import re_path
from django.urls import path
from roomerApi import consumers

websocket_urlpatterns = [
    path('ws/chat/<room_name>/', consumers.ChatConsumer.as_asgi()),
]
