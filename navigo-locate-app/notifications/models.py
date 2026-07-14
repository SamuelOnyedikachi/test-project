from django.db import models
from django.conf import settings


class Notification(models.Model):
    class Scope(models.TextChoices):
        SYSTEM = "system", "System"
        SAFETY = "safety", "Safety"
        TRACKING = "tracking", "Tracking"
        EMERGENCY = "emergency", "Emergency"
        ACCOUNT = "account", "Account"

    class Channel(models.TextChoices):
        PUSH = "push", "Push"
        SMS = "sms", "SMS"
        EMAIL = "email", "Email"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    channel = models.CharField(max_length=20, choices=Channel.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    scope = models.CharField(
        max_length=30,
        choices=Scope.choices,
        default=Scope.SYSTEM,
        help_text="Controls how the app categorizes and visually prioritizes this message.",
    )
    title = models.CharField(max_length=180)
    message = models.TextField()
    show_as_popup = models.BooleanField(
        default=True,
        help_text="Show this message as an in-app dialog the next time the recipient is active.",
    )
    recipient = models.CharField(max_length=180, blank=True)
    provider = models.CharField(max_length=80, blank=True)
    provider_message_id = models.CharField(max_length=180, blank=True)
    error_message = models.TextField(blank=True)
    payload = models.JSONField(
        default=dict,
        blank=True,
        help_text='Optional JSON such as {"type":"route.alert","session_id":12,"action_url":"/live-map"}. Never include passwords or secrets.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["channel", "status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.channel} - {self.status} - {self.title}"
