# Navigo Locate Deployment

Recommended production stack:

- Django + DRF + Channels
- Daphne ASGI server
- PostgreSQL + PostGIS
- Redis
- Nginx reverse proxy
- Cloudflare
- Object storage for media
- Firebase Cloud Messaging
- SMS gateway such as Termii, Africa's Talking, or Twilio

## Environment

Copy:

```bash
cp navigo-locate-app/.env.example .env
```

Set:

```text
SECRET_KEY=
DJANGO_DEBUG=False
ALLOWED_HOSTS=your-domain.com
POSTGRES_DB=navigo
POSTGRES_USER=navigo
POSTGRES_PASSWORD=
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_URL=redis://redis:6379/0
```

## Commands

```bash
docker compose build
docker compose up
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

## Services

```text
backend   Django + Daphne
db        PostgreSQL/PostGIS
redis     Channels layer and live cache
nginx     Public reverse proxy
```
