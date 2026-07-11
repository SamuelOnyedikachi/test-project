from rest_framework import serializers

from .models import TrustedContact


class TrustedContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustedContact
        fields = [
            "id",
            "name",
            "phone",
            "email",
            "role",
            "is_verified",
            "can_view_live_location",
            "can_view_route_history",
            "can_view_battery",
            "can_view_medical_info",
            "can_receive_sos",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "is_verified", "created_at", "updated_at"]
