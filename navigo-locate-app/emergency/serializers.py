from rest_framework import serializers

from .models import EmergencyIncident


class EmergencyIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyIncident
        fields = [
            "id",
            "user",
            "session",
            "status",
            "notes",
            "acknowledged_by",
            "acknowledged_at",
            "resolved_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "status",
            "acknowledged_by",
            "acknowledged_at",
            "resolved_at",
            "created_at",
            "updated_at",
        ]
