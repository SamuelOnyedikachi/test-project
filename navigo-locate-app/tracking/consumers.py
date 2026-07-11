from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from .models import TrackingSession
from .access import sessions_visible_to
from .realtime import tracking_group_name


class TrackingConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.group_name = tracking_group_name(self.session_id)
        self.user = self.scope.get("user", AnonymousUser())

        if not await self.can_view_session():
            await self.close(code=4403)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_json(
            {
                "type": "tracking.connected",
                "sessionId": self.session_id,
            }
        )

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def tracking_location(self, event):
        await self.send_json(event["payload"])

    @database_sync_to_async
    def can_view_session(self):
        if not self.user or not self.user.is_authenticated:
            return False

        return sessions_visible_to(self.user).filter(id=self.session_id).exists()
