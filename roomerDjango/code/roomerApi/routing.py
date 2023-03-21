
from django.urls import re_path
from django.urls import path
from roomerApi import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:donor_id>/<str:recipient_id>/', consumers.ChatConsumer.as_asgi()),
]
