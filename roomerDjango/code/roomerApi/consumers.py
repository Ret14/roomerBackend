import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers import serialize
from rest_framework.renderers import JSONRenderer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.donor_id = self.scope["url_route"]["kwargs"]["donor_id"]
        self.recipient_id = self.scope["url_route"]["kwargs"]["recipient_id"]
        self.room_group_name = "chat_%d" % (self.donor_id + self.recipient_id)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        from roomerApi.models import Profile
        from roomerApi.models import Message
        from roomerApi.models import Notification
        from roomerApi.serializers import ChatsSerializer
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        donor_id = text_data_json["donor_id"]
        recipient_id = text_data_json["recipient_id"]
        donor_profile = Profile.objects.get_queryset().filter(id=donor_id).first()
        recipient_profile = Profile.objects.get_queryset().filter(id=recipient_id).first()
        message_model = Message.objects.create(chat_id=donor_id + recipient_id, donor=donor_profile,
                                               recipient=recipient_profile, text=message,
                                               date_time=datetime.datetime.now())
        message_model.save()
        message = Message.objects.get(id=message_model.id)
        notification_model = Notification.objects.create(message=message)
        notification_model.save()
        serializer = ChatsSerializer(message)
        serialized = JSONRenderer().render(serializer.data)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": serialized}
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=message.decode())
