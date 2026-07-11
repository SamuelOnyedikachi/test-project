from django.urls import path

from .views import (
    EndTrackingSessionView,
    LiveTrackingView,
    LiveSnapshotView,
    RoutePointCreateView,
    RouteHistoryView,
    RouteReplayView,
    StartTrackingView,
    StopTrackingView,
    TrackingSessionDetailView,
    TrackingSessionListCreateView,
    UpdateLocationView,
)

urlpatterns = [
    path("start/", StartTrackingView.as_view(), name="tracking-start"),
    path("stop/", StopTrackingView.as_view(), name="tracking-stop"),
    path("update-location/", UpdateLocationView.as_view(), name="tracking-update-location"),
    path("live/<int:pk>/", LiveTrackingView.as_view(), name="tracking-live"),
    path(
        "live/<int:session_id>/snapshot/",
        LiveSnapshotView.as_view(),
        name="tracking-live-snapshot",
    ),
    path("history/", RouteHistoryView.as_view(), name="tracking-history"),
    path("history/<int:pk>/replay/", RouteReplayView.as_view(), name="tracking-replay"),
    path("sessions/", TrackingSessionListCreateView.as_view(), name="tracking-sessions"),
    path(
        "sessions/<int:pk>/",
        TrackingSessionDetailView.as_view(),
        name="tracking-session-detail",
    ),
    path(
        "sessions/<int:session_id>/locations/",
        RoutePointCreateView.as_view(),
        name="tracking-session-locations",
    ),
    path(
        "sessions/<int:session_id>/end/",
        EndTrackingSessionView.as_view(),
        name="tracking-session-end",
    ),
]
