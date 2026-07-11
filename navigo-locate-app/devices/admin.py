from django.contrib import admin

from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "platform",
        "name",
        "battery_level",
        "network_type",
        "last_seen_at",
        "is_active",
    )
    list_filter = ("platform", "is_active", "last_seen_at")
    list_editable = ("is_active",)
    search_fields = ("user__username", "user__email", "device_id", "name")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "last_seen_at"
    actions = ("deactivate_devices", "activate_devices")
    fieldsets = (
        ("Owner", {"fields": ("user",)}),
        ("Device", {"fields": ("device_id", "name", "platform", "is_active")}),
        ("Messaging", {"fields": ("fcm_token",)}),
        (
            "Telemetry",
            {
                "fields": (
                    "battery_level",
                    "network_type",
                    "last_latitude",
                    "last_longitude",
                    "last_seen_at",
                )
            },
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.action(description="Suspend selected devices")
    def deactivate_devices(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Reactivate selected devices")
    def activate_devices(self, request, queryset):
        queryset.update(is_active=True)
