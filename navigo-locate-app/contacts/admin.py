from django.contrib import admin

from .models import TrustedContact


@admin.register(TrustedContact)
class TrustedContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "name",
        "phone",
        "role",
        "is_verified",
        "can_receive_sos",
    )
    list_filter = ("role", "is_verified", "can_receive_sos")
    list_editable = ("role", "is_verified", "can_receive_sos")
    search_fields = ("owner__username", "owner__email", "name", "phone", "email")
    fieldsets = (
        ("Owner", {"fields": ("owner",)}),
        ("Contact", {"fields": ("name", "phone", "email", "role", "is_verified")}),
        (
            "Permissions",
            {
                "fields": (
                    "can_view_live_location",
                    "can_view_route_history",
                    "can_view_battery",
                    "can_view_medical_info",
                    "can_receive_sos",
                )
            },
        ),
    )
