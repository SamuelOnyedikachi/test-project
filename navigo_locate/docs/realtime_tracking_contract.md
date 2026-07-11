# Navigo Locate Realtime Tracking Contract

Navigo Locate treats the tracking engine as the core product. Maps are only a
visualization layer. Mobile apps, dashboards, and third-party systems should all
read and write through the same session, location, contact, and incident shapes.

## Firebase Realtime Database

Realtime data is optimized for fast updates and live map movement.

```text
tracking_sessions/{sessionId}
  sessionId: string
  userId: string
  status: "active" | "ended" | "expired"
  emergency: boolean
  startedAt: iso8601
  endedAt: iso8601?
  updatedAt: iso8601
  latest:
    latitude: number
    longitude: number
    accuracy: number
    altitude: number
    heading: number
    speed: number
    timestamp: iso8601
  route_points/{pushId}
    latitude: number
    longitude: number
    accuracy: number
    altitude: number
    heading: number
    speed: number
    timestamp: iso8601

emergency_incidents/{incidentId}
  incidentId: string
  sessionId: string
  userId: string
  status: "active" | "acknowledged" | "resolved" | "falseAlarm"
  createdAt: iso8601
  resolvedAt: iso8601?
  updatedAt: iso8601
```

## Permanent Backend API

The Django API should eventually store long-term records in PostgreSQL and expose
safe integration endpoints for other applications.

```text
POST /api/v1/tracking/sessions
GET  /api/v1/tracking/sessions/{sessionId}
POST /api/v1/tracking/sessions/{sessionId}/locations
GET  /api/v1/tracking/sessions/{sessionId}/stream
POST /api/v1/tracking/sessions/{sessionId}/end

POST /api/v1/emergency/incidents
GET  /api/v1/emergency/incidents/{incidentId}
POST /api/v1/emergency/incidents/{incidentId}/acknowledge
POST /api/v1/emergency/incidents/{incidentId}/resolve

GET  /api/v1/contacts
POST /api/v1/contacts
PATCH /api/v1/contacts/{contactId}/permissions
```

## Security Rules

Every location session must have:

- Explicit user ownership.
- Trusted-contact authorization before viewing.
- Expiry for shared links.
- Audit logs for every location view.
- Separate emergency permissions for responders.

## Update Cadence

The mobile app currently captures and publishes GPS every 2 seconds during an
active session. Production builds should later add:

- Battery-aware throttling.
- Offline queue and retry.
- Background tracking service.
- Batched permanent writes to PostgreSQL.
- Redis/WebSocket fanout for dashboards and third-party integrations.
