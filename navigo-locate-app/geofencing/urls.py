from django.urls import path

from .views import GeofenceDetailView, GeofenceEventListCreateView, GeofenceListCreateView

urlpatterns = [
    path("", GeofenceListCreateView.as_view(), name="geofences"),
    path("<int:pk>/", GeofenceDetailView.as_view(), name="geofence-detail"),
    path("events/", GeofenceEventListCreateView.as_view(), name="geofence-events"),
]
