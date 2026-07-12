import logging
import math

from audit.models import AuditLog
from django.core.cache import cache
from geofencing.models import Geofence, GeofenceEvent
from notifications.models import Notification

from .models import RoutePoint
from .realtime import broadcast_location_update

LIVE_LOCATION_CACHE_TTL_SECONDS = 60 * 60 * 24
logger = logging.getLogger(__name__)


def record_location_update(session, validated_data, actor=None, request=None):
    point = RoutePoint.objects.create(session=session, **validated_data)

    session.latest_latitude = point.latitude
    session.latest_longitude = point.longitude
    session.latest_accuracy = point.accuracy
    session.latest_speed = point.speed
    session.latest_heading = point.heading
    session.latest_altitude = point.altitude
    session.save(
        update_fields=[
            "latest_latitude",
            "latest_longitude",
            "latest_accuracy",
            "latest_speed",
            "latest_heading",
            "latest_altitude",
            "updated_at",
        ]
    )

    user = session.user
    user.last_latitude = point.latitude
    user.last_longitude = point.longitude
    user.save(update_fields=["last_latitude", "last_longitude"])

    _create_geofence_events(session, point)
    _create_audit_log(session, point, actor=actor, request=request)
    try:
        cache_live_location(session, point)
    except Exception:
        logger.exception("Unable to cache live location for session %s", session.id)
    try:
        broadcast_location_update(session, point)
    except Exception:
        logger.exception("Unable to broadcast live location for session %s", session.id)
    return point


def cache_live_location(session, point):
    cache.set(
        live_location_cache_key(session.id),
        {
            "session": {
                "id": session.id,
                "status": session.status,
                "emergency": session.emergency,
                "user_id": session.user_id,
                "started_at": session.started_at.isoformat(),
                "updated_at": session.updated_at.isoformat(),
            },
            "location": {
                "latitude": str(point.latitude),
                "longitude": str(point.longitude),
                "accuracy": point.accuracy,
                "altitude": point.altitude,
                "heading": point.heading,
                "speed": point.speed,
                "battery_level": point.battery_level,
                "network_type": point.network_type,
                "recorded_at": point.recorded_at.isoformat(),
            },
        },
        timeout=LIVE_LOCATION_CACHE_TTL_SECONDS,
    )


def get_cached_live_location(session_id):
    try:
        return cache.get(live_location_cache_key(session_id))
    except Exception:
        logger.exception("Unable to read cached location for session %s", session_id)
        return None


def sync_cached_session_status(session):
    payload = get_cached_live_location(session.id)
    if not payload:
        return

    payload["session"]["status"] = session.status
    payload["session"]["updated_at"] = session.updated_at.isoformat()
    if session.ended_at:
        payload["session"]["ended_at"] = session.ended_at.isoformat()
    try:
        cache.set(
            live_location_cache_key(session.id),
            payload,
            timeout=LIVE_LOCATION_CACHE_TTL_SECONDS,
        )
    except Exception:
        logger.exception("Unable to update cached status for session %s", session.id)


def live_location_cache_key(session_id):
    return f"tracking:live-location:{session_id}"


def _create_geofence_events(session, point):
    active_zones = Geofence.objects.filter(is_active=True).filter(owner__isnull=True) | Geofence.objects.filter(
        is_active=True,
        owner=session.user,
    )

    for geofence in active_zones.distinct():
        distance = _distance_meters(
            float(point.latitude),
            float(point.longitude),
            float(geofence.center_latitude),
            float(geofence.center_longitude),
        )
        if distance > geofence.radius_meters:
            continue

        exists = GeofenceEvent.objects.filter(
            geofence=geofence,
            user=session.user,
            event_type=GeofenceEvent.EventType.ENTER,
            occurred_at__date=point.recorded_at.date(),
        ).exists()
        if exists:
            continue

        GeofenceEvent.objects.create(
            geofence=geofence,
            user=session.user,
            event_type=GeofenceEvent.EventType.ENTER,
            latitude=point.latitude,
            longitude=point.longitude,
            occurred_at=point.recorded_at,
        )

        if geofence.zone_type == Geofence.ZoneType.DANGER:
            Notification.objects.create(
                user=session.user,
                channel=Notification.Channel.PUSH,
                status=Notification.Status.PENDING,
                title="Danger zone alert",
                message=f"{session.user.get_username()} entered {geofence.name}.",
                payload={
                    "type": "geofence.danger.enter",
                    "geofence_id": geofence.id,
                    "session_id": session.id,
                },
            )


def _create_audit_log(session, point, actor=None, request=None):
    AuditLog.objects.create(
        actor=actor or session.user,
        action="location.update",
        resource_type="tracking_session",
        resource_id=str(session.id),
        metadata={
            "route_point_id": point.id,
            "latitude": str(point.latitude),
            "longitude": str(point.longitude),
            "emergency": session.emergency,
        },
        ip_address=_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "") if request else "",
    )


def _client_ip(request):
    if request is None:
        return None
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _distance_meters(lat1, lon1, lat2, lon2):
    radius = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    return radius * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
