from django.db import models
from django.conf import settings


class TrustedContact(models.Model):
    class Role(models.TextChoices):
        FAMILY = "family", "Family"
        FRIEND = "friend", "Friend"
        RESPONDER = "responder", "Responder"
        ORGANIZATION = "organization", "Organization"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trusted_contacts",
    )
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.FAMILY)
    is_verified = models.BooleanField(default=False)

    can_view_live_location = models.BooleanField(default=True)
    can_view_route_history = models.BooleanField(default=True)
    can_view_battery = models.BooleanField(default=True)
    can_view_medical_info = models.BooleanField(default=False)
    can_receive_sos = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["owner", "role"]),
            models.Index(fields=["phone"]),
        ]
        unique_together = ("owner", "phone")

    def __str__(self):
        return f"{self.name} ({self.owner})"
