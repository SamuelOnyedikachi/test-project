from django.db import models
from django.conf import settings


class TrackingSession(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        ENDED = "ended", "Ended"
        EXPIRED = "expired", "Expired"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tracking_sessions",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )
    emergency = models.BooleanField(default=False, db_index=True)
    public_share_token = models.CharField(max_length=128, unique=True, blank=True, null=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    latest_latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    latest_longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    latest_accuracy = models.FloatField(null=True, blank=True)
    latest_speed = models.FloatField(null=True, blank=True)
    latest_heading = models.FloatField(null=True, blank=True)
    latest_altitude = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["emergency", "status"]),
            models.Index(fields=["started_at"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.status} - {self.started_at:%Y-%m-%d %H:%M}"


class RoutePoint(models.Model):
    session = models.ForeignKey(
        TrackingSession,
        on_delete=models.CASCADE,
        related_name="route_points",
    )
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    accuracy = models.FloatField(null=True, blank=True)
    altitude = models.FloatField(null=True, blank=True)
    heading = models.FloatField(null=True, blank=True)
    speed = models.FloatField(null=True, blank=True)
    battery_level = models.PositiveSmallIntegerField(null=True, blank=True)
    network_type = models.CharField(max_length=50, blank=True)
    recorded_at = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["recorded_at"]
        indexes = [
            models.Index(fields=["session", "recorded_at"]),
        ]

    def __str__(self):
        return f"{self.session_id} @ {self.recorded_at:%Y-%m-%d %H:%M:%S}"


class LocationViewAudit(models.Model):
    session = models.ForeignKey(
        TrackingSession,
        on_delete=models.CASCADE,
        related_name="view_audits",
    )
    viewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="location_views",
        null=True,
        blank=True,
    )
    api_key_name = models.CharField(max_length=120, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-viewed_at"]

    def __str__(self):
        return f"View of {self.session_id} at {self.viewed_at:%Y-%m-%d %H:%M}"


class DeveloperApiKey(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="developer_api_keys",
    )
    name = models.CharField(max_length=120)
    key_prefix = models.CharField(max_length=16, db_index=True)
    hashed_key = models.CharField(max_length=128)
    scopes = models.JSONField(default=list, blank=True)
    allowed_origins = models.JSONField(default=list, blank=True)
    allowed_ips = models.JSONField(default=list, blank=True)
    webhook_url = models.URLField(blank=True)
    rate_limit_per_minute = models.PositiveIntegerField(default=120)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.key_prefix})"
