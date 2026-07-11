from django.db import models
from django.conf import settings


class Device(models.Model):
    class Platform(models.TextChoices):
        ANDROID = "android", "Android"
        IOS = "ios", "iOS"
        WEB = "web", "Web"
        OTHER = "other", "Other"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="devices",
    )
    device_id = models.CharField(max_length=255)
    name = models.CharField(max_length=150, blank=True)
    platform = models.CharField(max_length=30, choices=Platform.choices, default=Platform.OTHER)
    fcm_token = models.TextField(blank=True)
    battery_level = models.PositiveSmallIntegerField(null=True, blank=True)
    network_type = models.CharField(max_length=50, blank=True)
    last_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    last_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_seen_at", "-created_at"]
        unique_together = ("user", "device_id")
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["device_id"]),
            models.Index(fields=["last_seen_at"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.platform} - {self.device_id}"
