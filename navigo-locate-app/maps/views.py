from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import MapProvider
from .serializers import MapProviderSerializer


class MapProviderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MapProviderSerializer
    queryset = MapProvider.objects.filter(is_active=True)
