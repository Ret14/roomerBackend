
from django.urls import re_path
from roomerApi import consumers

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<id_donor>)/(?P<id_recipient>)', consumers.ChatConsumer.as_asgi()),
]
