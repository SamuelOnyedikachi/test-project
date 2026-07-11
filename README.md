# Navigo Locate Platform

Navigo Locate is a realtime safety and location platform for individuals,
families, rescue teams, organizations, and authorized integrations. It combines
a Flutter client, a Django API and operations console, Redis-backed realtime
tracking, and a Neon PostgreSQL database.

This document is the operating handbook for the current platform. Features
described as planned are not yet production capabilities.

## Repository

```text
Navigo/
  navigo_locate/       Flutter mobile and web application
  navigo-locate-app/   Django API, admin console, and realtime engine
  docker/              Local Nginx configuration
  docs/                API, architecture, database, and deployment references
  docker-compose.yml   Local backend and infrastructure services
```

## Current Infrastructure

| Layer | Technology | Responsibility |
|---|---|---|
| Client | Flutter | Registration, login, tracking, contacts, history, SOS, destination tracking |
| API | Django 6 + Django REST Framework | Authentication, business rules, CRUD APIs, audit records |
| Realtime server | Daphne + Django Channels | ASGI HTTP and authenticated WebSocket connections |
| Live state | Redis | Current-location cache and WebSocket fanout |
| Durable database | Neon PostgreSQL | Users, sessions, route points, incidents, contacts, organizations |
| Operations console | Django Admin + Unfold | Administration, live map, agency assignment, incident operations |
| Operations map | Leaflet + OpenStreetMap | Active-session visualization for staff |
| Deployment | Railway | Backend container, public HTTPS domain, Redis service, migrations |
| Local edge | Nginx | Local reverse proxy for Docker development |
| Mobile services | Firebase configuration | Device messaging configuration and FCM token registration |

PostGIS, external SMS delivery, full push-delivery workers, and a separate
Next.js dashboard are planned extensions. The current database uses latitude,
longitude, and radius fields without PostGIS geometry types.

## System Flow

```text
Flutter device
    |
    | JWT-authenticated HTTPS
    v
Railway HTTPS edge
    |
    v
Daphne ASGI server
    |
    +--> Django REST API
    |       |
    |       +--> Neon PostgreSQL: durable users, sessions, points, history
    |       +--> Redis: latest live snapshot
    |       +--> Audit and geofence evaluation
    |
    +--> Django Channels
            |
            +--> Redis channel layer
            +--> Authorized owner/agency WebSocket viewers

Staff admin
    |
    +--> Live Operations Map
            |
            +--> Poll active session coordinates every five seconds
            +--> Assign rescue teams or organizations
```

### Authentication Flow

1. A user registers with username, email, optional profile fields, and password.
2. Login returns a JWT access token and refresh token.
3. The access token is sent as `Authorization: Bearer <token>` for API calls.
4. The refresh token obtains a new access token when the current one expires.
5. WebSocket clients pass the access token as `?token=<access-token>`.
6. Django admin uses a secure staff session rather than JWT.

### Tracking Flow

1. The client requests location permission and reads the current GPS position.
2. `POST /api/v1/tracking/start/` creates an active tracking session.
3. The client posts coordinates to `tracking/update-location/`.
4. Django saves every route point in Neon.
5. Django updates the session's latest coordinates and the user's last position.
6. Geofence rules are evaluated and audit records are written.
7. Redis stores the latest snapshot and broadcasts the update through Channels.
8. Authorized viewers read the snapshot or subscribe to the tracking WebSocket.
9. Stopping tracking marks the session ended and synchronizes cached status.

### Emergency Flow

1. The user starts SOS from the client.
2. Django creates an emergency tracking session and active incident.
3. Staff review the incident in the operations console.
4. A responder can acknowledge the incident.
5. Staff can assign an organization to the associated tracking session.
6. Operational members of that organization can monitor the assigned session.
7. Resolving or stopping SOS ends the associated active session.

### Agency Assignment Flow

1. A superuser creates an Organization.
2. User accounts are connected through Organization Members.
3. Each membership receives an organization role.
4. Staff open **Admin > Live Operations Map**.
5. Staff select one or more monitoring agencies on an active session.
6. Active operational members can read and subscribe to that session.
7. Removing the assignment immediately removes organization-based access.

## Roles and Permissions

### Platform Roles

| Role | Capabilities |
|---|---|
| Superuser | Full database administration, staff management, live operations, assignments, all admin models |
| Staff | Admin access granted by Django permissions; can use Live Operations and monitor all sessions |
| Regular user | Own profile, devices, contacts, tracking sessions, route history, notifications, and SOS |

### Organization Roles

| Role | Assigned-session monitoring | Typical responsibility |
|---|---:|---|
| Owner | Yes | Organization ownership and accountability |
| Admin | Yes | Membership and operational administration |
| Dispatcher | Yes | Monitor active users and coordinate response |
| Responder | Yes | Monitor an assigned user during field response |
| Member | No | Non-operational membership without location access |

Monitoring also requires an active membership and an explicit assignment of
the user's tracking session to the organization. A role alone does not expose
unassigned sessions.

### Trusted Contact Types

Trusted contacts are contact records, not authenticated platform roles:

- Family
- Friend
- Responder
- Organization

Each contact can be configured independently for live location, route history,
battery, medical information, and SOS notifications. A contact record does not
automatically create a user account or organization membership.

### Organization Types

- Rescue Team
- Company
- School
- Government
- Other

Organization type describes the entity. Organization role controls what a
specific member may do.

## Role Guides

### Regular User

1. Register or log in from the Flutter application.
2. Allow location access when prompted.
3. Open **Contacts** to add family, friends, responders, or organizations.
4. Select **Start Live Tracking** to create a session and publish movement.
5. Optionally enter a destination and coordinates before starting tracking.
6. Open **Live Map** to view current position, metrics, destination progress,
   and sharing controls.
7. Use **History** to inspect saved sessions and route points.
8. Use SOS for an emergency session and incident.
9. Stop tracking when the journey or emergency has ended.

The current destination feature provides bearing, remaining straight-line
distance, and progress. Turn-by-turn road routing requires a configured routing
provider and is not yet a complete production navigation engine.

### Superuser

1. Log in at `/admin/` using a superuser account.
2. Review platform metrics on the command center.
3. Create or manage users, devices, contacts, geofences, organizations, and API
   keys from their admin sections.
4. Create Organizations before assigning sessions to agencies.
5. Create Organization Members by selecting an organization, user, role, and
   active status.
6. Open `/admin/operations/live-tracking/` for the Live Operations Map.
7. Review active and SOS sessions, coordinates, accuracy, speed, and freshness.
8. Select monitoring agencies and submit **Update assignment**.
9. Review emergency incidents and update acknowledgement/resolution state.
10. Use audit logs and location-view audits to review sensitive access.

### Staff Administrator

1. A superuser creates the account and enables `is_staff`.
2. The superuser grants only the Django model permissions required by the job.
3. Staff log in through `/admin/`.
4. Staff can use Live Operations because all staff are trusted operational
   viewers, but other admin screens still follow Django model permissions.
5. Staff should not create superusers or change security settings unless their
   job explicitly requires it.

### Organization Owner or Admin

1. Ensure the account is an active member with Owner or Admin role.
2. The organization must be assigned to an active tracking session by staff.
3. Use the authenticated live tracking REST endpoint or WebSocket to monitor
   assigned sessions.
4. Do not share JWTs or location data outside the response operation.
5. Organization management through Django admin additionally requires staff
   status and the corresponding Django permissions.

### Dispatcher

1. Log in with an account linked to an active Dispatcher membership.
2. Receive the session ID through the operational assignment workflow.
3. Read `/tracking/live/{session_id}/` or its snapshot endpoint.
4. Subscribe to `/ws/tracking/{session_id}/?token=<jwt>` for live updates.
5. Coordinate responders and keep access limited to the active assignment.

### Responder

1. Log in with an active Responder membership.
2. Access only sessions explicitly assigned to the responder's organization.
3. Use live coordinates, accuracy, heading, and speed during response.
4. Acknowledge or resolve incidents only through an account/API flow authorized
   for that incident.
5. Stop using the location when the assignment or incident ends.

### Organization Member

A Member can belong to an organization but cannot monitor assigned live
sessions. Promote the membership to Responder, Dispatcher, Admin, or Owner only
when operational access is necessary.

### Developer/API Consumer

1. A user creates a Developer API Key in the admin or API.
2. The raw key is displayed only once and must be stored securely.
3. Configure scopes, allowed origins, allowed IPs, webhook URL, and rate limit.
4. Send the key using the API-key authentication format expected by the backend.
5. Rotate or deactivate compromised keys immediately.
6. Location reads are auditable and must follow the same privacy rules as staff.

## Admin Form Guide

All model forms use the Unfold admin base for consistent labels, spacing,
widgets, responsive layout, compressed fields, and unsaved-change warnings.

- Use search instead of scrolling through long change lists.
- Use filters for status, role, emergency state, and dates.
- Read-only timestamps and generated identifiers cannot be edited.
- Multi-select organization assignments appear on Tracking Session forms.
- Prefer the Live Operations Map for active-session assignment.
- Avoid changing ended sessions back to active unless correcting known data.

## API Overview

Base path:

```text
/api/v1/
```

Main modules:

```text
auth/             Registration, login, refresh, current user
devices/          Device registration and telemetry
tracking/         Sessions, location updates, live snapshots, history
emergency/        SOS and incident workflow
contacts/         Trusted contacts and sharing permissions
notifications/    Notification records
maps/             Configured map providers
geofences/        Zones and enter/exit events
organizations/    Organizations and memberships
developer/        Developer API keys
audit/            Audit-log reads
```

Detailed endpoints are documented in [docs/api-spec.md](docs/api-spec.md).

WebSockets:

```text
/ws/tracking/{session_id}/?token={jwt_access_token}
/ws/emergency/{incident_id}/?token={jwt_access_token}
/ws/dashboard/live/?token={jwt_access_token}
```

The dashboard WebSocket requires staff. Tracking access requires ownership,
staff status, or an active operational membership in an assigned organization.

## Local Development

### Backend services

```bash
cd /home/psalmcodes/Navigo
docker compose up -d --build backend redis nginx
docker compose exec backend python manage.py migrate
```

Local service addresses:

```text
Django API   http://localhost:8000
Nginx        http://localhost
Redis        redis://redis:6379/0 from Docker services
```

The root `.env` is loaded by Docker Compose. Never commit it.

### Flutter

```bash
cd /home/psalmcodes/Navigo/navigo_locate
flutter pub get
flutter run -d chrome \
  --web-port 8080 \
  --dart-define=NAVIGO_API_BASE_URL=http://localhost:8000/api/v1
```

Run static checks:

```bash
flutter analyze
```

## Railway Deployment

The backend contains `navigo-locate-app/railway.json` and a Dockerfile. Railway
runs migrations before starting Daphne and checks `/health/` before promoting a
deployment.

1. Push the monorepo to GitHub.
2. Create a Railway backend service from the repository.
3. Set Root Directory to `/navigo-locate-app`.
4. Add Neon variables to the backend service.
5. Add a Redis service in the same Railway project and environment.
6. Add a backend variable reference to `Redis.REDIS_URL`.
7. Generate a public Railway domain.
8. Deploy and verify `/health/` returns `{"status":"ok"}`.

Required backend variables:

```text
DJANGO_DEBUG=False
SECRET_KEY=<new-long-random-secret>
ALLOWED_HOSTS=healthcheck.railway.app

POSTGRES_DB=neondb
POSTGRES_USER=<Neon role>
POSTGRES_PASSWORD=<rotated Neon password>
POSTGRES_HOST=<Neon pooled host>
POSTGRES_PORT=5432
POSTGRES_SSLMODE=require
POSTGRES_CHANNEL_BINDING=require

REDIS_URL=${{Redis.REDIS_URL}}

CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=<Flutter web origin>
```

Do not use `redis://redis:6379/0` on Railway. That hostname belongs to local
Docker Compose. Use Railway's internal Redis variable reference.

Run Flutter against production:

```bash
flutter run -d chrome \
  --web-port 8080 \
  --dart-define=NAVIGO_API_BASE_URL=https://YOUR-DOMAIN.up.railway.app/api/v1
```

## Operational Checks

Health:

```bash
curl https://YOUR-DOMAIN.up.railway.app/health/
```

Redis from the Railway backend shell:

```bash
python manage.py shell -c "from django.core.cache import cache; cache.set('health','ok',30); print(cache.get('health'))"
```

Expected output is `ok`.

Database migrations:

```bash
python manage.py migrate
```

Expected output after deployment is `No migrations to apply.`

## Security and Privacy

- Never commit `.env`, database URLs, passwords, JWTs, Redis URLs, or API keys.
- Rotate any credential pasted into chat, logs, screenshots, or source control.
- Use a unique production `SECRET_KEY` and keep `DJANGO_DEBUG=False`.
- Grant staff and organization roles using least privilege.
- Organization membership does not grant location access without assignment.
- Member role never grants monitoring access.
- Remove agency assignments when response work ends.
- Review location-view and audit logs for inappropriate access.
- Treat coordinates, route history, contacts, and incident data as sensitive.
- Keep Neon SSL and channel binding required.

## Current Limitations

- Destination guidance is not full road-network turn-by-turn navigation.
- Trusted-contact sharing UI does not itself create authenticated contact access.
- Notification records exist, but complete provider delivery workers must be
  configured for production push, SMS, and email delivery.
- The admin map refreshes every five seconds; the tracking WebSocket supports
  realtime clients but the admin map currently uses polling.
- No self-service organization dashboard exists outside the API and admin.
- PostGIS spatial types and spatial indexes are planned rather than active.

## Additional Documentation

- [API specification](docs/api-spec.md)
- [Architecture](docs/architecture.md)
- [Database schema](docs/database-schema.md)
- [Deployment reference](docs/deployment.md)
- [Flutter realtime contract](navigo_locate/docs/realtime_tracking_contract.md)
