from django.db import models
from django.conf import settings


class Organization(models.Model):
    class OrganizationType(models.TextChoices):
        RESCUE = "rescue", "Rescue Team"
        COMPANY = "company", "Company"
        SCHOOL = "school", "School"
        GOVERNMENT = "government", "Government"
        OTHER = "other", "Other"

    name = models.CharField(max_length=180)
    organization_type = models.CharField(
        max_length=30,
        choices=OrganizationType.choices,
        default=OrganizationType.OTHER,
    )
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["organization_type", "is_verified"]),
        ]

    def __str__(self):
        return self.name


class OrganizationMember(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        DISPATCHER = "dispatcher", "Dispatcher"
        RESPONDER = "responder", "Responder"
        MEMBER = "member", "Member"

    OPERATIONAL_ROLES = (
        Role.OWNER,
        Role.ADMIN,
        Role.DISPATCHER,
        Role.RESPONDER,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="members",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organization_memberships",
    )
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.MEMBER)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("organization", "user")
        indexes = [
            models.Index(fields=["organization", "role"]),
            models.Index(fields=["user", "is_active"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.organization} ({self.role})"
