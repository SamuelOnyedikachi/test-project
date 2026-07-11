from django.db import models
from django.conf import settings


class Geofence(models.Model):
    class ZoneType(models.TextChoices):
        SAFE = "safe", "Safe Zone"
        DANGER = "danger", "Danger Zone"
        CUSTOM = "custom", "Custom Zone"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="geofences",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=150)
    zone_type = models.CharField(max_length=20, choices=ZoneType.choices, default=ZoneType.CUSTOM)
    center_latitude = models.DecimalField(max_digits=10, decimal_places=7)
    center_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    radius_meters = models.PositiveIntegerField(default=250)
    is_public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["zone_type", "is_active"]),
            models.Index(fields=["owner", "is_active"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.zone_type})"


class GeofenceEvent(models.Model):
    class EventType(models.TextChoices):
        ENTER = "enter", "Enter"
        EXIT = "exit", "Exit"

    geofence = models.ForeignKey(
        Geofence,
        on_delete=models.CASCADE,
        related_name="events",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="geofence_events",
    )
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    occurred_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-occurred_at"]
        indexes = [
            models.Index(fields=["user", "occurred_at"]),
            models.Index(fields=["geofence", "occurred_at"]),
        ]

    def __str__(self):
        return f"{self.user} {self.event_type} {self.geofence}"
