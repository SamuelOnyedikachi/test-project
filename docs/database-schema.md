# Navigo Locate Database Schema

Production database: PostgreSQL with PostGIS planned.

Local development database: SQLite fallback.

## Core Tables

```text
accounts_user
devices_device
contacts_trustedcontact
tracking_trackingsession
tracking_routepoint
tracking_locationviewaudit
tracking_developerapikey
emergency_emergencyincident
notifications_notification
geofencing_geofence
geofencing_geofenceevent
organizations_organization
organizations_organizationmember
maps_mapprovider
audit_auditlog
```

## Tracking

`tracking_trackingsession` stores the current live session and latest known
position. `tracking_routepoint` stores durable route history.

The mobile app should send:

```json
{
  "session_id": 1,
  "latitude": 6.5244,
  "longitude": 3.3792,
  "accuracy": 8.2,
  "altitude": 41.0,
  "heading": 190.0,
  "speed": 2.4,
  "battery_level": 78,
  "network_type": "4g",
  "recorded_at": "2026-07-05T12:00:00Z"
}
```

## Geofencing

Current geofence storage uses center latitude, center longitude, and radius. When
PostGIS is enabled, this should move to geometry/geography columns for efficient
spatial queries.

## Audit

Audit records should be written whenever:

- A user views a live location.
- A responder accesses an emergency incident.
- A developer API key reads location data.
- An admin changes incident, contact, or organization permissions.
