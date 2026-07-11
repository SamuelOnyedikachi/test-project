from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Geofence, GeofenceEvent
from .serializers import GeofenceEventSerializer, GeofenceSerializer


class GeofenceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GeofenceSerializer

    def get_queryset(self):
        return Geofence.objects.filter(Q(owner=self.request.user) | Q(is_public=True))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GeofenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GeofenceSerializer

    def get_queryset(self):
        return Geofence.objects.filter(owner=self.request.user)


class GeofenceEventListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GeofenceEventSerializer

    def get_queryset(self):
        return GeofenceEvent.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
