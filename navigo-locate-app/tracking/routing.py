from django.urls import path

from .dashboard_consumers import DashboardLiveConsumer
from .consumers import TrackingConsumer

websocket_urlpatterns = [
    path("ws/tracking/<int:session_id>/", TrackingConsumer.as_asgi()),
    path("ws/dashboard/live/", DashboardLiveConsumer.as_asgi()),
]
