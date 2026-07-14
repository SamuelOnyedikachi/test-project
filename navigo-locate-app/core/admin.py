import re
import math
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils import timezone
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
                "operations/live-tracking/assign/",
                self.admin_view(self.assign_tracking_organizations),
                name="live-tracking-assign",
            ),
        ]
        return custom_urls + super().get_urls()

    def live_tracking_view(self, request):
        google_map_id = settings.GOOGLE_MAP_ID.strip()
        if not re.fullmatch(r"[0-9a-fA-F]{16}", google_map_id):
            google_map_id = ""
        context = {
            **self.each_context(request),
            "title": "Live Operations",
            "data_url": reverse("admin:live-tracking-data"),
            "assign_url": reverse("admin:live-tracking-assign"),
            "google_maps_web_api_key": settings.GOOGLE_MAPS_WEB_API_KEY,
            "google_map_id": google_map_id,
            "organizations": Organization.objects.order_by("name"),
        }
        return TemplateResponse(request, "admin/live_tracking.html", context)

    def live_tracking_data(self, request):
        fresh_after = timezone.now() - timedelta(minutes=5)
        sessions = (
            TrackingSession.objects.filter(
                status=TrackingSession.Status.ACTIVE,
                updated_at__gte=fresh_after,
            )
            .select_related("user")
            .prefetch_related(
                "assigned_organizations",
                Prefetch(
                    "route_points",
                    queryset=RoutePoint.objects.order_by("-recorded_at")[:60],
                    to_attr="recent_route_points",
                ),
            )
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
                        "route": self._route_segments(session),
                        "organizations": [
                            {"id": organization.id, "name": organization.name}
                            for organization in session.assigned_organizations.all()
                        ],
                    }
                    for session in sessions
                ]
            }
        )

    @staticmethod
    def _route_segments(session):
        points = list(reversed(session.recent_route_points))
        result = []
        total_distance = 0.0
        previous = None
        for point in points:
            distance = 0.0
            duration = 0.0
            if previous is not None:
                distance = _distance_meters(
                    float(previous.latitude),
                    float(previous.longitude),
                    float(point.latitude),
                    float(point.longitude),
                )
                duration = max(0.0, (point.recorded_at - previous.recorded_at).total_seconds())
                total_distance += distance
            result.append(
                {
                    "id": point.id,
                    "latitude": float(point.latitude),
                    "longitude": float(point.longitude),
                    "accuracy": point.accuracy,
                    "recorded_at": point.recorded_at.isoformat(),
                    "distance_meters": round(distance, 2),
                    "duration_seconds": round(duration, 1),
                    "total_distance_meters": round(total_distance, 2),
                }
            )
            previous = point
        return result

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


def _distance_meters(lat1, lon1, lat2, lon2):
    radius = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    value = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    return radius * 2 * math.atan2(math.sqrt(value), math.sqrt(1 - value))
navigo_admin_site.register(Organization, OrganizationAdmin)
navigo_admin_site.register(OrganizationMember, OrganizationMemberAdmin)
