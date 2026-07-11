from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tracking.models import TrackingSession

from .models import EmergencyIncident
from .serializers import EmergencyIncidentSerializer


class EmergencyIncidentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmergencyIncidentSerializer

    def get_queryset(self):
        return EmergencyIncident.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        session = serializer.validated_data["session"]
        if session.user_id != self.request.user.id:
            raise PermissionDenied("You can only create incidents for your own sessions.")
        session.emergency = True
        session.save(update_fields=["emergency", "updated_at"])
        serializer.save(user=self.request.user)


class EmergencyIncidentDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmergencyIncidentSerializer

    def get_queryset(self):
        return EmergencyIncident.objects.filter(user=self.request.user)


class AcknowledgeIncidentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, incident_id):
        incident = generics.get_object_or_404(
            EmergencyIncident,
            id=incident_id,
            user=request.user,
        )
        incident.status = EmergencyIncident.Status.ACKNOWLEDGED
        incident.acknowledged_by = request.user
        incident.acknowledged_at = timezone.now()
        incident.save(
            update_fields=[
                "status",
                "acknowledged_by",
                "acknowledged_at",
                "updated_at",
            ]
        )
        return Response(EmergencyIncidentSerializer(incident).data)


class ResolveIncidentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, incident_id):
        incident = generics.get_object_or_404(
            EmergencyIncident,
            id=incident_id,
            user=request.user,
        )
        incident.status = EmergencyIncident.Status.RESOLVED
        incident.resolved_at = timezone.now()
        incident.save(update_fields=["status", "resolved_at", "updated_at"])

        session = incident.session
        if session.status == TrackingSession.Status.ACTIVE:
            session.status = TrackingSession.Status.ENDED
            session.ended_at = incident.resolved_at
            session.save(update_fields=["status", "ended_at", "updated_at"])

        return Response(
            EmergencyIncidentSerializer(incident).data,
            status=status.HTTP_200_OK,
        )


class StartSosView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        session = TrackingSession.objects.create(
            user=request.user,
            emergency=True,
            status=TrackingSession.Status.ACTIVE,
        )
        incident = EmergencyIncident.objects.create(
            user=request.user,
            session=session,
            status=EmergencyIncident.Status.ACTIVE,
            notes=request.data.get("notes", ""),
        )
        request.user.is_emergency_active = True
        request.user.save(update_fields=["is_emergency_active"])
        return Response(
            EmergencyIncidentSerializer(incident).data,
            status=status.HTTP_201_CREATED,
        )


class StopSosView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        incident_id = request.data.get("incident_id")
        incident = generics.get_object_or_404(
            EmergencyIncident,
            id=incident_id,
            user=request.user,
            status__in=[
                EmergencyIncident.Status.ACTIVE,
                EmergencyIncident.Status.ACKNOWLEDGED,
            ],
        )
        incident.status = EmergencyIncident.Status.RESOLVED
        incident.resolved_at = timezone.now()
        incident.save(update_fields=["status", "resolved_at", "updated_at"])

        session = incident.session
        if session.status == TrackingSession.Status.ACTIVE:
            session.status = TrackingSession.Status.ENDED
            session.ended_at = incident.resolved_at
            session.save(update_fields=["status", "ended_at", "updated_at"])

        request.user.is_emergency_active = False
        request.user.save(update_fields=["is_emergency_active"])
        return Response(EmergencyIncidentSerializer(incident).data)
