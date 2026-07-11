import secrets

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from tracking.models import DeveloperApiKey


class DeveloperApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperApiKey
        fields = [
            "id",
            "name",
            "key_prefix",
            "scopes",
            "allowed_origins",
            "allowed_ips",
            "webhook_url",
            "rate_limit_per_minute",
            "notes",
            "is_active",
            "created_at",
            "last_used_at",
        ]
        read_only_fields = ["id", "key_prefix", "created_at", "last_used_at"]


class DeveloperApiKeyCreateSerializer(serializers.ModelSerializer):
    raw_key = serializers.CharField(read_only=True)

    class Meta:
        model = DeveloperApiKey
        fields = ["id", "name", "key_prefix", "raw_key", "created_at"]
        read_only_fields = ["id", "key_prefix", "raw_key", "created_at"]

    def create(self, validated_data):
        raw_key = f"nvg_{secrets.token_urlsafe(32)}"
        validated_data["key_prefix"] = raw_key[:12]
        validated_data["hashed_key"] = make_password(raw_key)
        instance = super().create(validated_data)
        instance.raw_key = raw_key
        return instance
