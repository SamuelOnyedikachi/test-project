from rest_framework import serializers

from .models import MapProvider


class MapProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapProvider
        fields = [
            "id",
            "name",
            "provider",
            "is_active",
            "supports_routing",
            "supports_traffic",
            "supports_places",
            "configuration",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
