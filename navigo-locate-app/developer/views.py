from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from tracking.models import DeveloperApiKey

from .serializers import DeveloperApiKeyCreateSerializer, DeveloperApiKeySerializer


class DeveloperApiKeyListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DeveloperApiKey.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return DeveloperApiKeyCreateSerializer
        return DeveloperApiKeySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DeveloperApiKeyDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeveloperApiKeySerializer

    def get_queryset(self):
        return DeveloperApiKey.objects.filter(owner=self.request.user)
