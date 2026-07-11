# Navigo Locate API Spec

Base URL:

```text
/api/v1/
```

## Auth

```text
POST /auth/register/
POST /auth/login/
POST /auth/refresh/
GET  /auth/me/
```

## Devices

```text
GET    /devices/
POST   /devices/
GET    /devices/{id}/
PATCH  /devices/{id}/
DELETE /devices/{id}/
```

## Tracking Engine

```text
POST /tracking/start/
POST /tracking/stop/
POST /tracking/update-location/
GET  /tracking/live/{session_id}/
GET  /tracking/live/{session_id}/snapshot/
GET  /tracking/history/
GET  /tracking/history/{session_id}/replay/
GET  /tracking/sessions/
POST /tracking/sessions/
GET  /tracking/sessions/{session_id}/
POST /tracking/sessions/{session_id}/locations/
POST /tracking/sessions/{session_id}/end/
```

## Emergency

```text
POST /emergency/sos/start/
POST /emergency/sos/stop/
GET  /emergency/incidents/
POST /emergency/incidents/
GET  /emergency/incidents/{incident_id}/
POST /emergency/incidents/{incident_id}/acknowledge/
POST /emergency/incidents/{incident_id}/resolve/
```

## Contacts

```text
GET    /contacts/
POST   /contacts/
GET    /contacts/{id}/
PATCH  /contacts/{id}/
DELETE /contacts/{id}/
```

## Geofences

```text
GET    /geofences/
POST   /geofences/
GET    /geofences/{id}/
PATCH  /geofences/{id}/
DELETE /geofences/{id}/
GET    /geofences/events/
POST   /geofences/events/
```

## Organizations

```text
GET   /organizations/
POST  /organizations/
GET   /organizations/{id}/
PATCH /organizations/{id}/
GET   /organizations/members/
POST  /organizations/members/
```

## Developer Platform

```text
GET    /developer/api-keys/
POST   /developer/api-keys/
GET    /developer/api-keys/{id}/
PATCH  /developer/api-keys/{id}/
DELETE /developer/api-keys/{id}/
```

## Maps

```text
GET /maps/providers/
```

## Audit

```text
GET /audit/
```

## WebSockets

```text
/ws/tracking/{session_id}/?token={jwt_access_token}
/ws/emergency/{incident_id}/?token={jwt_access_token}
/ws/dashboard/live/?token={jwt_access_token}
```
