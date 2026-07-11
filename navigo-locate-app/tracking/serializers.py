from rest_framework import serializers

from .models import DeveloperApiKey, LocationViewAudit, RoutePoint, TrackingSession


class RoutePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutePoint
        fields = [
            "id",
            "session",
            "latitude",
            "longitude",
            "accuracy",
            "altitude",
            "heading",
            "speed",
            "battery_level",
            "network_type",
            "recorded_at",
            "created_at",
        ]
        read_only_fields = ["id", "session", "created_at"]


class TrackingSessionSerializer(serializers.ModelSerializer):
    route_points_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = TrackingSession
        fields = [
            "id",
            "user",
            "assigned_organizations",
            "status",
            "emergency",
            "public_share_token",
            "expires_at",
            "started_at",
            "ended_at",
            "updated_at",
            "latest_latitude",
            "latest_longitude",
            "latest_accuracy",
            "latest_speed",
            "latest_heading",
            "latest_altitude",
            "route_points_count",
        ]
        read_only_fields = [
            "id",
            "user",
            "assigned_organizations",
            "status",
            "started_at",
            "ended_at",
            "updated_at",
            "latest_latitude",
            "latest_longitude",
            "latest_accuracy",
            "latest_speed",
            "latest_heading",
            "latest_altitude",
            "route_points_count",
        ]


class TrackingSessionDetailSerializer(TrackingSessionSerializer):
    route_points = RoutePointSerializer(many=True, read_only=True)

    class Meta(TrackingSessionSerializer.Meta):
        fields = TrackingSessionSerializer.Meta.fields + ["route_points"]


class RouteHistorySerializer(serializers.ModelSerializer):
    route_points = RoutePointSerializer(many=True, read_only=True)

    class Meta:
        model = TrackingSession
        fields = [
            "id",
            "user",
            "assigned_organizations",
            "status",
            "emergency",
            "started_at",
            "ended_at",
            "latest_latitude",
            "latest_longitude",
            "route_points",
        ]


class LocationViewAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationViewAudit
        fields = [
            "id",
            "session",
            "viewer",
            "api_key_name",
            "ip_address",
            "user_agent",
            "viewed_at",
        ]
        read_only_fields = fields


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
