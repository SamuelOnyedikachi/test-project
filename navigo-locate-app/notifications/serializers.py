from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "channel",
            "status",
            "scope",
            "title",
            "message",
            "show_as_popup",
            "recipient",
            "provider",
            "provider_message_id",
            "error_message",
            "payload",
            "created_at",
            "sent_at",
            "read_at",
        ]
        read_only_fields = ["id", "status", "provider_message_id", "error_message", "created_at", "sent_at", "read_at"]
