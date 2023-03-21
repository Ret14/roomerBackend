
from django.urls import path
from roomerApi import consumers

websocket_urlpatterns = [
    path("ws://176.113.83.93:8000/ws/chat/<int:donor_id>/<int:recipient_id>/", consumers.ChatConsumer.as_asgi())
    #re_path(r"ws/chat/(?P<donor_id>)/(?P<recipient_id>)/$", consumers.ChatConsumer.as_asgi()),
]
