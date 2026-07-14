from django.conf import settings
from django.contrib import admin
from unfold.admin import ModelAdmin

from .forms import GeofenceAdminForm
from .models import Geofence, GeofenceEvent


@admin.register(Geofence)
class GeofenceAdmin(ModelAdmin):
    form = GeofenceAdminForm
    change_form_template = "admin/geofencing/geofence/change_form.html"
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ("id", "name", "zone_type", "shape_type", "owner", "radius_meters", "is_public", "is_active")
    list_filter = ("zone_type", "shape_type", "is_public", "is_active")
    list_editable = ("zone_type", "is_public", "is_active")
    search_fields = ("name", "owner__username", "address", "description")
    fieldsets = (
        ("Owner", {"fields": ("owner",)}),
        ("Zone", {"fields": ("name", "zone_type", "description", "is_public", "is_active")}),
        (
            "Map boundary",
            {
                "fields": (
                    "shape_type",
                    "address",
                    "center_latitude",
                    "center_longitude",
                    "radius_meters",
                    "north_latitude",
                    "south_latitude",
                    "east_longitude",
                    "west_longitude",
                ),
                "description": "Use the map below to place and resize the boundary. Coordinates and measurements update automatically.",
            },
        ),
    )

    def get_changeform_initial_data(self, request):
        return {
            **super().get_changeform_initial_data(request),
            "center_latitude": 9.0820,
            "center_longitude": 8.6753,
            "radius_meters": 250,
        }

    def render_change_form(self, request, context, *args, **kwargs):
        context["google_maps_web_api_key"] = settings.GOOGLE_MAPS_WEB_API_KEY
        return super().render_change_form(request, context, *args, **kwargs)


@admin.register(GeofenceEvent)
class GeofenceEventAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ("id", "geofence", "user", "event_type", "occurred_at")
    list_filter = ("event_type", "occurred_at")
    search_fields = ("geofence__name", "user__username")
    readonly_fields = ("created_at",)
