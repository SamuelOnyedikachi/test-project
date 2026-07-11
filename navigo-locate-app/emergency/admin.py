from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import EmergencyIncident


@admin.register(EmergencyIncident)
class EmergencyIncidentAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = (
        "id",
        "user",
        "session",
        "status",
        "acknowledged_by",
        "created_at",
        "resolved_at",
    )
    list_filter = ("status", "created_at", "resolved_at")
    list_editable = ("status",)
    search_fields = ("user__username", "user__email", "user__phone", "notes")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Incident", {"fields": ("user", "session", "status", "notes")}),
        ("Responder", {"fields": ("acknowledged_by", "acknowledged_at", "resolved_at")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
