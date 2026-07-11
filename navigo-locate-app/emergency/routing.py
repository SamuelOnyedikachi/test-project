from django.urls import path

from .consumers import EmergencyConsumer

websocket_urlpatterns = [
    path("ws/emergency/<int:incident_id>/", EmergencyConsumer.as_asgi()),
]
