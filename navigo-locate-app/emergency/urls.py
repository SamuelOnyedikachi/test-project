from django.urls import path

from .views import (
    AcknowledgeIncidentView,
    EmergencyIncidentDetailView,
    EmergencyIncidentListCreateView,
    ResolveIncidentView,
    StartSosView,
    StopSosView,
)

urlpatterns = [
    path("sos/start/", StartSosView.as_view(), name="sos-start"),
    path("sos/stop/", StopSosView.as_view(), name="sos-stop"),
    path("incidents/", EmergencyIncidentListCreateView.as_view(), name="incidents"),
    path(
        "incidents/<int:pk>/",
        EmergencyIncidentDetailView.as_view(),
        name="incident-detail",
    ),
    path(
        "incidents/<int:incident_id>/acknowledge/",
        AcknowledgeIncidentView.as_view(),
        name="incident-acknowledge",
    ),
    path(
        "incidents/<int:incident_id>/resolve/",
        ResolveIncidentView.as_view(),
        name="incident-resolve",
    ),
]
