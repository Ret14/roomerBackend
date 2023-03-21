
from django.urls import re_path
from django.urls import path
from roomerApi import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:donor_id>/<int:recipient_id>', consumers.ChatConsumer.as_asgi()),
]
