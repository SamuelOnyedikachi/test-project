from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import TrustedContact
from .serializers import TrustedContactSerializer


class TrustedContactListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrustedContactSerializer

    def get_queryset(self):
        return TrustedContact.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TrustedContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrustedContactSerializer

    def get_queryset(self):
        return TrustedContact.objects.filter(owner=self.request.user)
