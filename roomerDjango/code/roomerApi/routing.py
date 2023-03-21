from django.template.defaulttags import url
from django.urls import re_path
from roomerApi import consumers

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]
