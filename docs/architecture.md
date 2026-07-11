# Navigo Locate Platform Architecture

Navigo Locate is a tracking engine first. Google Maps, Mapbox, and
OpenStreetMap are visualization clients, not the product core.

```text
                    Navigo Platform
                         |
      +------------------+------------------+
      |                  |                  |
 Flutter App       Rescue Dashboard    Public API
      |                  |                  |
      +------------------+------------------+
                         |
                  Tracking Engine
                         |
        Django + DRF + Channels + Redis
                         |
              PostgreSQL + PostGIS
                         |
        Google Maps / Mapbox / OpenStreetMap
```

## Runtime Flow

```text
GPS Device / Flutter App
        |
        | every 2 seconds
        v
REST or WebSocket Tracking Gateway
        |
        +--> Redis live snapshot cache
        |
        +--> Redis WebSocket fanout
        |
        +--> PostgreSQL durable route history
        |
        v
Viewer App / Rescue Dashboard / Trusted Contact
```

## Current Repository

```text
Navigo/
  navigo_locate/       Flutter mobile app
  navigo-locate-app/   Django backend API and realtime engine
  docs/                Platform architecture documentation
```

## Target Repository Shape

```text
navigo-locate-platform/
  mobile/
  backend/
  dashboard/
  docs/
  docker/
  infrastructure/
  scripts/
```

## Backend Responsibilities

- Authentication and roles.
- Registered devices and FCM tokens.
- Tracking sessions.
- Live location update ingestion.
- Route history.
- Redis live location snapshots for dashboards and developer API clients.
- SOS incidents.
- Trusted contacts and permissions.
- Location view audit logs.
- Developer API keys.
- WebSocket broadcast.
- Future geofencing and PostGIS spatial search.

## API Surface

```text
/api/v1/accounts/register/
/api/v1/accounts/login/
/api/v1/accounts/refresh/
/api/v1/accounts/me/

/api/v1/tracking/start/
/api/v1/tracking/stop/
/api/v1/tracking/update-location/
/api/v1/tracking/live/{session_id}/
/api/v1/tracking/live/{session_id}/snapshot/
/api/v1/tracking/history/
/api/v1/tracking/history/{session_id}/replay/
/api/v1/tracking/sessions/

/api/v1/emergency/incidents/
/api/v1/emergency/incidents/{id}/acknowledge/
/api/v1/emergency/incidents/{id}/resolve/

/api/v1/contacts/
```

## WebSocket Surface

```text
/ws/tracking/{session_id}/?token={jwt_access_token}
```

## Database Strategy

Local development can use SQLite. Production should use PostgreSQL with PostGIS.
Redis is required in production for live location cache and multi-process
WebSocket fanout.
