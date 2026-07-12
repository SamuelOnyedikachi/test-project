from django.db.models import Count
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LocationViewAudit, RoutePoint, TrackingSession
from .access import sessions_visible_to
from .services import get_cached_live_location, record_location_update, sync_cached_session_status
from .serializers import (
    RouteHistorySerializer,
    RoutePointSerializer,
    TrackingSessionDetailSerializer,
    TrackingSessionSerializer,
)


class TrackingSessionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrackingSessionSerializer

    def get_queryset(self):
        return (
            TrackingSession.objects.filter(user=self.request.user)
            .annotate(route_points_count=Count("route_points"))
            .order_by("-started_at")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TrackingSessionDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrackingSessionDetailSerializer

    def get_queryset(self):
        return TrackingSession.objects.filter(user=self.request.user).prefetch_related(
            "route_points"
        )


class RoutePointCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoutePointSerializer

    def perform_create(self, serializer):
        session = generics.get_object_or_404(
            TrackingSession,
            id=self.kwargs["session_id"],
            user=self.request.user,
            status=TrackingSession.Status.ACTIVE,
        )
        point = record_location_update(
            session,
            serializer.validated_data,
            actor=self.request.user,
            request=self.request,
        )


class EndTrackingSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        session = generics.get_object_or_404(
            TrackingSession,
            id=session_id,
            user=request.user,
            status=TrackingSession.Status.ACTIVE,
        )
        session.status = TrackingSession.Status.ENDED
        session.ended_at = timezone.now()
        session.save(update_fields=["status", "ended_at", "updated_at"])
        sync_cached_session_status(session)
        return Response(TrackingSessionSerializer(session).data, status=status.HTTP_200_OK)


class StartTrackingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TrackingSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        previous_sessions = TrackingSession.objects.filter(
            user=request.user,
            status=TrackingSession.Status.ACTIVE,
        )
        for previous_session in previous_sessions:
            previous_session.status = TrackingSession.Status.ENDED
            previous_session.ended_at = timezone.now()
            previous_session.save(
                update_fields=["status", "ended_at", "updated_at"]
            )
            sync_cached_session_status(previous_session)
        session = serializer.save(user=request.user)
        return Response(
            TrackingSessionSerializer(session).data,
            status=status.HTTP_201_CREATED,
        )


class StopTrackingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        session_id = request.data.get("session_id")
        session = generics.get_object_or_404(
            TrackingSession,
            id=session_id,
            user=request.user,
            status=TrackingSession.Status.ACTIVE,
        )
        session.status = TrackingSession.Status.ENDED
        session.ended_at = timezone.now()
        session.save(update_fields=["status", "ended_at", "updated_at"])
        sync_cached_session_status(session)
        return Response(TrackingSessionSerializer(session).data)


class UpdateLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        session_id = request.data.get("session_id")
        session = generics.get_object_or_404(
            TrackingSession,
            id=session_id,
            user=request.user,
            status=TrackingSession.Status.ACTIVE,
        )
        serializer = RoutePointSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        point = record_location_update(
            session,
            serializer.validated_data,
            actor=request.user,
            request=request,
        )
        return Response(RoutePointSerializer(point).data, status=status.HTTP_201_CREATED)


class LiveTrackingView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrackingSessionSerializer

    def get_queryset(self):
        return sessions_visible_to(self.request.user).annotate(
            route_points_count=Count("route_points")
        )

    def retrieve(self, request, *args, **kwargs):
        session = self.get_object()
        record_location_view(session, request)
        serializer = self.get_serializer(session)
        return Response(serializer.data)


class LiveSnapshotView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        session = generics.get_object_or_404(
            sessions_visible_to(request.user),
            id=session_id,
        )
        record_location_view(session, request)

        cached_snapshot = get_cached_live_location(session.id)
        if cached_snapshot:
            cached_snapshot["source"] = "cache"
            return Response(cached_snapshot)

        return Response(
            {
                "source": "database",
                "session": {
                    "id": session.id,
                    "status": session.status,
                    "emergency": session.emergency,
                    "user_id": session.user_id,
                    "started_at": session.started_at.isoformat(),
                    "updated_at": session.updated_at.isoformat(),
                    "ended_at": session.ended_at.isoformat() if session.ended_at else None,
                },
                "location": {
                    "latitude": str(session.latest_latitude)
                    if session.latest_latitude is not None
                    else None,
                    "longitude": str(session.latest_longitude)
                    if session.latest_longitude is not None
                    else None,
                    "accuracy": session.latest_accuracy,
                    "altitude": session.latest_altitude,
                    "heading": session.latest_heading,
                    "speed": session.latest_speed,
                },
            }
        )


class RouteHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrackingSessionSerializer

    def get_queryset(self):
        return (
            TrackingSession.objects.filter(user=self.request.user)
            .annotate(route_points_count=Count("route_points"))
            .order_by("-started_at")
        )


class RouteReplayView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RouteHistorySerializer

    def get_queryset(self):
        return TrackingSession.objects.filter(user=self.request.user).prefetch_related(
            "route_points"
        )

    def retrieve(self, request, *args, **kwargs):
        session = self.get_object()
        record_location_view(session, request)
        serializer = self.get_serializer(session)
        return Response(serializer.data)


def record_location_view(session, request):
    api_key = getattr(request, "developer_api_key", None)
    LocationViewAudit.objects.create(
        session=session,
        viewer=request.user if request.user.is_authenticated else None,
        api_key_name=api_key.name if api_key else "",
        ip_address=client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
    )


def client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")
