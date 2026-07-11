from django.contrib import admin

from .models import Geofence, GeofenceEvent


@admin.register(Geofence)
class GeofenceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "zone_type", "owner", "radius_meters", "is_public", "is_active")
    list_filter = ("zone_type", "is_public", "is_active")
    list_editable = ("zone_type", "radius_meters", "is_public", "is_active")
    search_fields = ("name", "owner__username", "description")
    fieldsets = (
        ("Owner", {"fields": ("owner",)}),
        ("Zone", {"fields": ("name", "zone_type", "description", "is_public", "is_active")}),
        ("Boundary", {"fields": ("center_latitude", "center_longitude", "radius_meters")}),
    )


@admin.register(GeofenceEvent)
class GeofenceEventAdmin(admin.ModelAdmin):
    list_display = ("id", "geofence", "user", "event_type", "occurred_at")
    list_filter = ("event_type", "occurred_at")
    search_fields = ("geofence__name", "user__username")
    readonly_fields = ("created_at",)
