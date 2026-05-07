from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AdminConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add("admin", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("admin", self.channel_name)

    async def send_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))
