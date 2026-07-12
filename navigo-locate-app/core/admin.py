import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.views.decorators.http import require_POST
from unfold.admin import ModelAdmin
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

    def get_urls(self):
        custom_urls = [
            path(
                "operations/live-tracking/",
                self.admin_view(self.live_tracking_view),
                name="live-tracking",
            ),
            path(
                "operations/live-tracking/data/",
                self.admin_view(self.live_tracking_data),
                name="live-tracking-data",
            ),
            path(
                "operations/live-tracking/places/",
                self.admin_view(self.live_tracking_places),
                name="live-tracking-places",
            ),
            path(
                "operations/live-tracking/assign/",
                self.admin_view(self.assign_tracking_organizations),
                name="live-tracking-assign",
            ),
        ]
        return custom_urls + super().get_urls()

    def live_tracking_view(self, request):
        context = {
            **self.each_context(request),
            "title": "Live Operations",
            "data_url": reverse("admin:live-tracking-data"),
            "places_url": reverse("admin:live-tracking-places"),
            "assign_url": reverse("admin:live-tracking-assign"),
            "organizations": Organization.objects.order_by("name"),
        }
        return TemplateResponse(request, "admin/live_tracking.html", context)

    def live_tracking_data(self, request):
        sessions = (
            TrackingSession.objects.filter(status=TrackingSession.Status.ACTIVE)
            .select_related("user")
            .prefetch_related("assigned_organizations")
            .order_by("-emergency", "-updated_at")
        )
        return JsonResponse(
            {
                "sessions": [
                    {
                        "id": session.id,
                        "user": session.user.get_full_name()
                        or session.user.get_username(),
                        "username": session.user.get_username(),
                        "emergency": session.emergency,
                        "latitude": float(session.latest_latitude)
                        if session.latest_latitude is not None
                        else None,
                        "longitude": float(session.latest_longitude)
                        if session.latest_longitude is not None
                        else None,
                        "accuracy": session.latest_accuracy,
                        "speed": session.latest_speed,
                        "heading": session.latest_heading,
                        "updated_at": session.updated_at.isoformat(),
                        "organizations": [
                            {"id": organization.id, "name": organization.name}
                            for organization in session.assigned_organizations.all()
                        ],
                    }
                    for session in sessions
                ]
            }
        )

    def live_tracking_places(self, request):
        try:
            south, west, north, east = [
                float(value) for value in request.GET["bbox"].split(",")
            ]
        except (KeyError, TypeError, ValueError):
            return JsonResponse({"error": "A valid bbox is required."}, status=400)

        if (
            south >= north
            or west >= east
            or north - south > 0.5
            or east - west > 0.5
            or not (-90 <= south <= 90 and -90 <= north <= 90)
            or not (-180 <= west <= 180 and -180 <= east <= 180)
        ):
            return JsonResponse({"error": "The requested map area is too large."}, status=400)

        bbox = f"{south:.5f},{west:.5f},{north:.5f},{east:.5f}"
        cache_key = f"admin:places:{bbox}"
        try:
            cached = cache.get(cache_key)
        except Exception:
            cached = None
        if cached is not None:
            return JsonResponse(cached)

        amenities = (
            "fuel|hospital|clinic|doctors|pharmacy|townhall|community_centre|"
            "social_centre|events_venue|conference_centre|police|fire_station|"
            "school|college|university"
        )
        query = (
            "[out:json][timeout:15];("
            f'nwr["amenity"~"^({amenities})$"]({bbox});'
            f'nwr["tourism"~"^(attraction|museum|gallery)$"]({bbox});'
            f'nwr["historic"]["name"]({bbox});'
            ");out center 200;"
        )
        url = "https://overpass-api.de/api/interpreter?" + urlencode({"data": query})
        overpass_request = Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "NaviGo-Locate/1.0 (+https://navigo-locate-production.up.railway.app)",
            },
        )
        try:
            with urlopen(overpass_request, timeout=20) as response:
                payload = json.load(response)
        except (URLError, TimeoutError, ValueError):
            return JsonResponse(
                {"error": "Nearby places are temporarily unavailable."},
                status=502,
            )

        try:
            cache.set(cache_key, payload, timeout=60)
        except Exception:
            pass
        return JsonResponse(payload)

    @require_POST
    def assign_tracking_organizations(self, request):
        session = TrackingSession.objects.filter(
            pk=request.POST.get("session_id"),
            status=TrackingSession.Status.ACTIVE,
        ).first()
        if session is None:
            messages.error(request, "The tracking session is no longer active.")
            return redirect("admin:live-tracking")

        organizations = Organization.objects.filter(
            pk__in=request.POST.getlist("organization_ids")
        )
        session.assigned_organizations.set(organizations)
        messages.success(request, "Monitoring agencies updated.")
        return redirect("admin:live-tracking")

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
                "label": "Live Operations Map",
                "url": reverse("admin:live-tracking"),
                "description": "Monitor active users and assign response agencies.",
            },
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


class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    compressed_fields = True

navigo_admin_site.register(get_user_model(), CustomUserAdmin)
navigo_admin_site.register(Group, GroupAdmin)
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
