from django import forms

from .models import Geofence


class GeofenceAdminForm(forms.ModelForm):
    class Meta:
        model = Geofence
        fields = "__all__"
        help_texts = {
            "owner": "Leave empty for a platform-wide geofence, or select one user for a private zone.",
            "is_public": "Public zones are visible to authenticated users through the geofence API.",
            "is_active": "Only active zones are evaluated against incoming live locations.",
            "description": "Explain the purpose, access rules, or response expected when this boundary is crossed.",
        }
