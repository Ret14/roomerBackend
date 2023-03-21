
from django.urls import re_path
from roomerApi import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<donor_id>)/(?P<recipient_id>)/$", consumers.ChatConsumer.as_asgi()),
]
