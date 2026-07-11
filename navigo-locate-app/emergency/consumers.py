from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from .models import EmergencyIncident


class EmergencyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.incident_id = self.scope["url_route"]["kwargs"]["incident_id"]
        self.group_name = f"emergency.incident.{self.incident_id}"
        self.user = self.scope.get("user", AnonymousUser())

        if not await self.can_view_incident():
            await self.close(code=4403)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_json(
            {
                "type": "emergency.connected",
                "incidentId": self.incident_id,
            }
        )

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    @database_sync_to_async
    def can_view_incident(self):
        if not self.user or not self.user.is_authenticated:
            return False

        return EmergencyIncident.objects.filter(
            id=self.incident_id,
            user=self.user,
        ).exists()
