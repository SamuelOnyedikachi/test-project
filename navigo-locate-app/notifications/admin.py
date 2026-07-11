from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ("id", "user", "channel", "status", "title", "created_at", "sent_at")
    list_filter = ("channel", "status", "created_at")
    list_editable = ("status",)
    search_fields = ("user__username", "recipient", "title", "message")
    readonly_fields = ("created_at", "sent_at")
    fieldsets = (
        ("Recipient", {"fields": ("user", "recipient", "channel", "status")}),
        ("Content", {"fields": ("title", "message", "payload")}),
        ("Provider", {"fields": ("provider", "provider_message_id", "error_message")}),
        ("Timeline", {"fields": ("created_at", "sent_at")}),
    )
