import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers import serialize


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
        from django.forms.models import model_to_dict
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
        notification_model = Notification.objects.create(message=Message.objects.get(id=message_model.id))
        notification_model.save()
        serialized = json.dumps(message_model.__dict__)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": serialized}
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=message)
