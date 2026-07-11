from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Device
from .serializers import DeviceSerializer


class DeviceListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, last_seen_at=timezone.now())


class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)


class DeviceRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        device, _ = Device.objects.update_or_create(
            user=request.user,
            device_id=data["device_id"],
            defaults={
                **data,
                "user": request.user,
                "last_seen_at": timezone.now(),
                "is_active": True,
            },
        )

        user_update_fields = []
        if device.fcm_token:
            request.user.fcm_token = device.fcm_token
            user_update_fields.append("fcm_token")
        request.user.device_id = device.device_id
        user_update_fields.append("device_id")
        if device.last_latitude is not None:
            request.user.last_latitude = device.last_latitude
            user_update_fields.append("last_latitude")
        if device.last_longitude is not None:
            request.user.last_longitude = device.last_longitude
            user_update_fields.append("last_longitude")
        request.user.save(update_fields=user_update_fields)

        return Response(DeviceSerializer(device).data)
