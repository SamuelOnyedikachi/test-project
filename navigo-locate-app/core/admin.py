from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from unfold.sites import UnfoldAdminSite

from accounts.admin import CustomUserAdmin
from contacts.models import TrustedContact
from contacts.admin import TrustedContactAdmin
from devices.models import Device
from devices.admin import DeviceAdmin
from emergency.models import EmergencyIncident
from emergency.admin import EmergencyIncidentAdmin
from geofencing.models import Geofence
from geofencing.admin import GeofenceAdmin, GeofenceEventAdmin
from geofencing.models import GeofenceEvent
from maps.admin import MapProviderAdmin
from maps.models import MapProvider
from notifications.admin import NotificationAdmin
from notifications.models import Notification
from organizations.models import Organization
from organizations.admin import OrganizationAdmin, OrganizationMemberAdmin
from organizations.models import OrganizationMember
from tracking.admin import (
    DeveloperApiKeyAdmin,
    LocationViewAuditAdmin,
    RoutePointAdmin,
    TrackingSessionAdmin,
)
from tracking.models import (
    DeveloperApiKey,
    LocationViewAudit,
    RoutePoint,
    TrackingSession,
)


class NavigoAdminSite(UnfoldAdminSite):
    site_header = "Navigo Locate"
    site_title = "Navigo Locate Admin"
    index_title = "Operations Command Center"

    def index(self, request, extra_context=None):
        User = get_user_model()
        extra_context = extra_context or {}
        extra_context["navigo_metrics"] = [
            {
                "label": "Active Tracking",
                "value": TrackingSession.objects.filter(
                    status=TrackingSession.Status.ACTIVE
                ).count(),
                "tone": "primary",
            },
            {
                "label": "Active SOS",
                "value": EmergencyIncident.objects.filter(
                    status=EmergencyIncident.Status.ACTIVE
                ).count(),
                "tone": "danger",
            },
            {
                "label": "Route Points",
                "value": RoutePoint.objects.count(),
                "tone": "success",
            },
            {
                "label": "Registered Devices",
                "value": Device.objects.filter(is_active=True).count(),
                "tone": "neutral",
            },
            {
                "label": "Trusted Contacts",
                "value": TrustedContact.objects.count(),
                "tone": "neutral",
            },
            {
                "label": "Users",
                "value": User.objects.count(),
                "tone": "neutral",
            },
            {
                "label": "Geofences",
                "value": Geofence.objects.filter(is_active=True).count(),
                "tone": "neutral",
            },
            {
                "label": "Organizations",
                "value": Organization.objects.count(),
                "tone": "neutral",
            },
        ]
        extra_context["navigo_quick_links"] = [
            {
                "label": "Tracking Sessions",
                "url": "tracking/trackingsession/",
                "description": "Monitor live and historical location sessions.",
            },
            {
                "label": "Emergency Incidents",
                "url": "emergency/emergencyincident/",
                "description": "Review SOS events and responder activity.",
            },
            {
                "label": "Route Points",
                "url": "tracking/routepoint/",
                "description": "Inspect stored GPS movement history.",
            },
            {
                "label": "Trusted Contacts",
                "url": "contacts/trustedcontact/",
                "description": "Manage who can receive alerts and view sessions.",
            },
        ]
        return super().index(request, extra_context=extra_context)


navigo_admin_site = NavigoAdminSite(name="admin")

navigo_admin_site.register(get_user_model(), CustomUserAdmin)
navigo_admin_site.register(Group)
navigo_admin_site.register(Device, DeviceAdmin)
navigo_admin_site.register(TrackingSession, TrackingSessionAdmin)
navigo_admin_site.register(RoutePoint, RoutePointAdmin)
navigo_admin_site.register(LocationViewAudit, LocationViewAuditAdmin)
navigo_admin_site.register(DeveloperApiKey, DeveloperApiKeyAdmin)
navigo_admin_site.register(EmergencyIncident, EmergencyIncidentAdmin)
navigo_admin_site.register(TrustedContact, TrustedContactAdmin)
navigo_admin_site.register(Notification, NotificationAdmin)
navigo_admin_site.register(MapProvider, MapProviderAdmin)
navigo_admin_site.register(Geofence, GeofenceAdmin)
navigo_admin_site.register(GeofenceEvent, GeofenceEventAdmin)
navigo_admin_site.register(Organization, OrganizationAdmin)
navigo_admin_site.register(OrganizationMember, OrganizationMemberAdmin)
