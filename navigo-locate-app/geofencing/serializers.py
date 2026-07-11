from rest_framework import serializers

from .models import Geofence, GeofenceEvent


class GeofenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geofence
        fields = [
            "id",
            "name",
            "zone_type",
            "center_latitude",
            "center_longitude",
            "radius_meters",
            "is_public",
            "is_active",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class GeofenceEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeofenceEvent
        fields = [
            "id",
            "geofence",
            "event_type",
            "latitude",
            "longitude",
            "occurred_at",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
