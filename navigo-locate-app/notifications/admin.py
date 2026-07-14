from django.contrib import admin
from unfold.admin import ModelAdmin

from .forms import NotificationAdminForm
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    form = NotificationAdminForm
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ("id", "user", "scope", "channel", "status", "title", "show_as_popup", "created_at", "read_at")
    list_filter = ("scope", "channel", "status", "show_as_popup", "created_at")
    list_editable = ("status",)
    search_fields = ("user__username", "recipient", "title", "message")
    readonly_fields = ("created_at", "sent_at", "read_at")
    fieldsets = (
        ("Audience", {"fields": ("audience", "user", "selected_users", "recipient")}),
        ("Delivery", {"fields": ("channel", "status", "scope", "show_as_popup")}),
        ("Content", {"fields": ("title", "message", "payload"), "description": "Payload must be valid JSON. Scope controls category; payload supplies optional action context."}),
        ("Provider", {"fields": ("provider", "provider_message_id", "error_message")}),
        ("Timeline", {"fields": ("created_at", "sent_at", "read_at")}),
    )

    def save_model(self, request, obj, form, change):
        if change:
            super().save_model(request, obj, form, change)
            return

        recipients = form.recipients()
        obj.user = recipients[0]
        if obj.channel == Notification.Channel.PUSH and not obj.provider:
            obj.provider = "in_app"
        super().save_model(request, obj, form, change)
        copied_fields = (
            "channel", "status", "scope", "title", "message", "show_as_popup",
            "recipient", "provider", "provider_message_id", "error_message", "payload", "sent_at",
        )
        values = {name: getattr(obj, name) for name in copied_fields}
        Notification.objects.bulk_create(
            [Notification(user=user, **values) for user in recipients[1:]]
        )
