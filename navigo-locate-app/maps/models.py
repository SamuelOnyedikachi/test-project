from django.db import models


class MapProvider(models.Model):
    class Provider(models.TextChoices):
        GOOGLE = "google_maps", "Google Maps"
        MAPBOX = "mapbox", "Mapbox"
        OPENSTREETMAP = "openstreetmap", "OpenStreetMap"

    name = models.CharField(max_length=80)
    provider = models.CharField(max_length=40, choices=Provider.choices, unique=True)
    is_active = models.BooleanField(default=True)
    supports_routing = models.BooleanField(default=True)
    supports_traffic = models.BooleanField(default=False)
    supports_places = models.BooleanField(default=False)
    configuration = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
