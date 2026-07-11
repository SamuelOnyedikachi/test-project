# Navigo Locate Backend

Django REST backend for Navigo Locate realtime tracking, emergency incidents,
trusted contacts, audit logs, and future third-party integrations.

## Database

Development currently uses SQLite through Django's default local configuration.
Production should use PostgreSQL.

Why PostgreSQL:

- Durable storage for incidents, route history, contacts, audit logs, and API keys.
- Strong relational integrity for ownership and permissions.
- Easy upgrade path to PostGIS for geofencing, nearby responders, danger zones,
  and spatial queries.

Recommended production stack:

- PostgreSQL for permanent records.
- Redis for live-session cache and WebSocket fanout.
- Firebase Realtime Database or WebSockets for low-latency mobile map updates.
- PostGIS when geofencing, danger zones, and nearby responder queries begin.

## Core API

```text
POST /api/v1/accounts/register/
POST /api/v1/accounts/login/
POST /api/v1/accounts/refresh/
GET  /api/v1/accounts/me/

GET  /api/v1/tracking/sessions/
POST /api/v1/tracking/sessions/
GET  /api/v1/tracking/sessions/{id}/
POST /api/v1/tracking/sessions/{id}/locations/
POST /api/v1/tracking/sessions/{id}/end/
POST /api/v1/tracking/start/
POST /api/v1/tracking/stop/
POST /api/v1/tracking/update-location/
GET  /api/v1/tracking/live/{id}/

GET  /api/v1/emergency/incidents/
POST /api/v1/emergency/incidents/
GET  /api/v1/emergency/incidents/{id}/
POST /api/v1/emergency/incidents/{id}/acknowledge/
POST /api/v1/emergency/incidents/{id}/resolve/

GET  /api/v1/contacts/
POST /api/v1/contacts/
GET  /api/v1/contacts/{id}/
PATCH /api/v1/contacts/{id}/
DELETE /api/v1/contacts/{id}/
```

## WebSockets

Live viewers subscribe to tracking sessions through Django Channels:

```text
ws://localhost:8000/ws/tracking/{session_id}/?token={jwt_access_token}
```

When the mobile app posts a new route point, the backend broadcasts:

```json
{
  "type": "location.update",
  "session": {
    "id": 1,
    "status": "active",
    "emergency": false,
    "userId": 1
  },
  "location": {
    "latitude": 6.5244,
    "longitude": 3.3792,
    "accuracy": 8.3,
    "altitude": 41.2,
    "heading": 182.0,
    "speed": 2.4,
    "batteryLevel": 73,
    "networkType": "4g",
    "recordedAt": "2026-07-05T12:00:00+00:00"
  }
}
```

## Next Infrastructure Step

Configure the `POSTGRES_*` environment variables before deployment. The backend
uses SQLite only when `POSTGRES_DB` is empty.
