from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def tracking_group_name(session_id):
    return f"tracking.session.{session_id}"


def broadcast_location_update(session, point):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    payload = {
        "type": "location.update",
        "session": {
            "id": session.id,
            "status": session.status,
            "emergency": session.emergency,
            "userId": session.user_id,
        },
        "location": {
            "latitude": float(point.latitude),
            "longitude": float(point.longitude),
            "accuracy": point.accuracy,
            "altitude": point.altitude,
            "heading": point.heading,
            "speed": point.speed,
            "batteryLevel": point.battery_level,
            "networkType": point.network_type,
            "recordedAt": point.recorded_at.isoformat(),
        },
    }

    async_to_sync(channel_layer.group_send)(
        tracking_group_name(session.id),
        {
            "type": "tracking.location",
            "payload": payload,
        },
    )

    broadcast_dashboard_event(
        {
            "type": "dashboard.location_update",
            "session": payload["session"],
            "location": payload["location"],
        }
    )


def broadcast_dashboard_event(payload):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    async_to_sync(channel_layer.group_send)(
        "dashboard.live",
        {
            "type": "dashboard.event",
            "payload": payload,
        },
    )
