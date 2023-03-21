import json
import uuid

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        global clients
        clients[scope["user"]] = self.channel_name
        await self.send_json({"type": "welcome"})

    async def disconnect(self, **kwargs):
        pass

    async def receive_json(self, content, **kwargs):
        global chats, clients
        if content["type"] == "invite":
            chat = str(uuid.uuid4())
            chats.append(chat)
            for member in content["members"]:
                self.channel_layer.send(clients[member], {
                    "type": "invite",
                    "id": chat
                })
        if content["type"] == "disconnect":
            self.channel_layer.group_send(content["id"], {
                "type": "disconnect",
                "id": content["id"]
            })
            chats.remove(content["id"])
        if content["type"] == "notify":
            # входящее сообщение от клиента
            self.channel_layer.group_send(content["id"], {
                "type": "notify",
                "kind": content.kind,
                "message": content.message,
                "sender": self.channel_name
            })

    async def chat_message(self, event):
        # пересылаем клиенту внутреннее сообщение о приглашении в группу
        if event["type"] == "invite":
            # добавимся также в группу
            await self.group_add(event["id"], self.channel_name)
            await self.send_json(event)
        if event["type"] == "disconnect":
            # отключаемся от группы
            await self.group_discard(event["id"], self.channel_name)
        if event["type"] == "notify":
            if event["sender"] != self.channel_name:
                self.send_json(event)
