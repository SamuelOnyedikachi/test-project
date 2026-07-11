from rest_framework import serializers

from .models import Organization, OrganizationMember


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "organization_type",
            "phone",
            "email",
            "address",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "is_verified", "created_at", "updated_at"]


class OrganizationMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationMember
        fields = [
            "id",
            "organization",
            "user",
            "role",
            "is_active",
            "joined_at",
        ]
        read_only_fields = ["id", "user", "joined_at"]
