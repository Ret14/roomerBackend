import json

from channels.generic.websocket import AsynkWebsocketConsumer


class ChatConsumer(AsynkWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'type': 'received_message',
            'message': message,
        }))

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message}))
