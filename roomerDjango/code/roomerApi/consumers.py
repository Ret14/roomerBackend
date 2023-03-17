import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({
            'type': 'received_message',
            'message': text_data,
        }))

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message}))
