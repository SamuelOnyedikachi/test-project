from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MapProvider
from .serializers import MapProviderSerializer
from .services import reverse_geocode


class MapProviderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MapProviderSerializer
    queryset = MapProvider.objects.filter(is_active=True)


class ReverseGeocodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            latitude = float(request.query_params["latitude"])
            longitude = float(request.query_params["longitude"])
        except (KeyError, TypeError, ValueError):
            return Response(
                {"detail": "Valid latitude and longitude query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
            return Response(
                {"detail": "Coordinates are outside the valid latitude/longitude range."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            return Response(reverse_geocode(latitude, longitude))
        except RuntimeError as error:
            return Response({"detail": str(error)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except (LookupError, OSError) as error:
            return Response({"detail": str(error)}, status=status.HTTP_502_BAD_GATEWAY)
