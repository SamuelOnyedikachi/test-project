from channels.generic.websocket import AsyncJsonWebsocketConsumer


class DashboardLiveConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or not user.is_authenticated or not user.is_staff:
            await self.close(code=4403)
            return

        await self.channel_layer.group_add("dashboard.live", self.channel_name)
        await self.accept()
        await self.send_json({"type": "dashboard.connected"})

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("dashboard.live", self.channel_name)

    async def dashboard_event(self, event):
        await self.send_json(event["payload"])
