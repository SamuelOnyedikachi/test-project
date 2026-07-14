from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Geofence(models.Model):
    class ShapeType(models.TextChoices):
        CIRCLE = "circle", "Circle"
        RECTANGLE = "rectangle", "Rectangle"
        SQUARE = "square", "Square"

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
    shape_type = models.CharField(
        max_length=20,
        choices=ShapeType.choices,
        default=ShapeType.CIRCLE,
        help_text="Choose a circle, rectangle, or equal-sided square boundary.",
    )
    center_latitude = models.DecimalField(max_digits=10, decimal_places=7)
    center_longitude = models.DecimalField(max_digits=10, decimal_places=7)
    radius_meters = models.PositiveIntegerField(
        default=250,
        help_text="Circle radius in meters. Rectangle and square maps update this to the center-to-corner distance.",
    )
    north_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    south_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    east_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    west_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    address = models.CharField(
        max_length=500,
        blank=True,
        help_text="Nearest building, street, locality/LGA, state, and country returned by Google Maps.",
    )
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

    def clean(self):
        super().clean()
        if self.shape_type == self.ShapeType.CIRCLE:
            return

        bounds = (
            self.north_latitude,
            self.south_latitude,
            self.east_longitude,
            self.west_longitude,
        )
        if any(value is None for value in bounds):
            raise ValidationError("Rectangle and square geofences require all four map bounds.")
        if self.north_latitude <= self.south_latitude:
            raise ValidationError({"north_latitude": "North latitude must be above south latitude."})
        if self.east_longitude <= self.west_longitude:
            raise ValidationError({"east_longitude": "East longitude must be east of west longitude."})


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
