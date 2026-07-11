# Navigo Locate Platform

Navigo Locate is a realtime location intelligence platform for safety,
emergency response, family monitoring, organizations, and future third-party
integrations.

The product is the tracking engine. Google Maps, Mapbox, and OpenStreetMap are
visualization layers.

## Current Structure

```text
Navigo/
  navigo_locate/       Flutter mobile app
  navigo-locate-app/   Django API and realtime engine
  docs/                Architecture, API, database, deployment
```

## Target Platform

```text
Mobile App       Flutter
Backend API      Django + DRF
Realtime Engine  Django Channels + Redis
Database         PostgreSQL + PostGIS
Notifications    FCM + SMS gateway
Dashboard        Next.js
Infrastructure   Docker + Nginx + Cloudflare
```


Run services:
cd /home/psalmcodes/Navigo
docker compose up -d --build backend redis nginx
docker compose exec backend python manage.py migrate


Run the Flutter app in another terminal:
cd /home/psalmcodes/Navigo/navigo_locate
flutter pub get
flutter run -d chrome \
  --dart-define=NAVIGO_API_BASE_URL=http://localhost:8000/api/v1

## Deploy the Backend on Railway

The backend includes `railway.json` for Docker builds, database migrations,
and health checks. Neon remains the PostgreSQL host.

1. Push this repository to GitHub.
2. Create a Railway project and add a service from the GitHub repository.
3. Set the service Root Directory to `/navigo-locate-app`.
4. Add the production environment variables documented below.
5. Add Railway Redis and reference its `REDIS_URL` from the backend service.
6. Generate a public domain under **Settings > Networking**.

Backend service variables:

```text
DJANGO_DEBUG=False
SECRET_KEY=<generate a new production secret>
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
CORS_ALLOWED_ORIGINS=http://localhost:8080
```

`RAILWAY_PUBLIC_DOMAIN` is provided automatically and Django adds it to its
allowed hosts. Replace or extend `CORS_ALLOWED_ORIGINS` with the deployed
Flutter web origin when the frontend is hosted.

After deployment, run Flutter against the Railway URL:

```bash
flutter run -d chrome \
  --web-port 8080 \
  --dart-define=NAVIGO_API_BASE_URL=https://YOUR-DOMAIN.up.railway.app/api/v1
```
