import json

from channels.generic.websocket import AsyncWebsocketConsumer


class DispatchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.rider_id = self.scope["user"].id
        self.group_name = f"rider_{self.rider_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Message from rider {self.rider_id}: {data}")
        await self.send(text_data=json.dumps({"status": "received"}))

    async def send_dispatch(self, event):
        await self.send(text_data=json.dumps(event))
