from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import MapProvider


@admin.register(MapProvider)
class MapProviderAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = ("id", "name", "provider", "is_active", "supports_routing", "supports_traffic")
    list_filter = ("provider", "is_active", "supports_routing", "supports_traffic")
    list_editable = ("is_active", "supports_routing", "supports_traffic")
    search_fields = ("name", "provider")
    fieldsets = (
        ("Provider", {"fields": ("name", "provider", "is_active")}),
        ("Capabilities", {"fields": ("supports_routing", "supports_traffic", "supports_places")}),
        ("Configuration", {"fields": ("configuration",)}),
    )
