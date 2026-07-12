from pathlib import Path
from datetime import timedelta
from decouple import config
from django.templatetags.static import static

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-6yhb#f13y1%^f5+tkm3s!8mg_ecs(07=jj!zt4531#xczt!vc#',
)
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = [
    host.strip()
    for host in config('ALLOWED_HOSTS', default='*').split(',')
    if host.strip()
]
RAILWAY_PUBLIC_DOMAIN = config('RAILWAY_PUBLIC_DOMAIN', default='')
if RAILWAY_PUBLIC_DOMAIN and RAILWAY_PUBLIC_DOMAIN not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RAILWAY_PUBLIC_DOMAIN)
if not DEBUG:
    for railway_host in ('.up.railway.app', 'healthcheck.railway.app'):
        if railway_host not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(railway_host)

INSTALLED_APPS = [
    'unfold',
    'daphne',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'channels',

    'accounts',
    'devices',
    'tracking',
    'emergency',
    'contacts',
    'notifications',
    'maps',
    'geofencing',
    'organizations',
    'audit',
    'developer',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

if config('POSTGRES_DB', default=''):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('POSTGRES_DB'),
            'USER': config('POSTGRES_USER'),
            'PASSWORD': config('POSTGRES_PASSWORD'),
            'HOST': config('POSTGRES_HOST', default='localhost'),
            'PORT': config('POSTGRES_PORT', default='5432'),
            'OPTIONS': {
                'sslmode': config('POSTGRES_SSLMODE', default='prefer'),
                'channel_binding': config(
                    'POSTGRES_CHANNEL_BINDING', default='prefer'
                ),
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

REDIS_URL = config('REDIS_URL', default='')

if REDIS_URL:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [REDIS_URL],
            },
        },
    }
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
        },
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'navigo-dev-cache',
        },
    }

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

UNFOLD = {
    'SITE_TITLE': 'Navigo Locate',
    'SITE_HEADER': 'Navigo Command Center',
    'SITE_SUBHEADER': 'Realtime safety, tracking, and rescue operations',
    'SITE_ICON': lambda request: static('branding/logo.png'),
    'SITE_FAVICONS': [
        {
            'rel': 'icon',
            'type': 'image/png',
            'href': lambda request: static('branding/logo.png'),
        },
    ],
    'SITE_SYMBOL': 'shield',
    'SHOW_HISTORY': True,
    'SHOW_VIEW_ON_SITE': False,
    'COLORS': {
        'primary': {
            '50': '239 246 255',
            '100': '219 234 254',
            '200': '191 219 254',
            '300': '147 197 253',
            '400': '96 165 250',
            '500': '15 98 254',
            '600': '0 67 206',
            '700': '6 60 159',
            '800': '7 43 97',
            '900': '7 23 51',
            '950': '2 8 23',
        },
    },
    'SIDEBAR': {
        'show_search': True,
        'show_all_applications': True,
        'navigation': [
            {
                'title': 'Operations',
                'separator': True,
                'items': [
                    {
                        'title': 'Live Operations Map',
                        'icon': 'location_searching',
                        'link': '/admin/operations/live-tracking/',
                    },
                    {
                        'title': 'Tracking Sessions',
                        'icon': 'route',
                        'link': '/admin/tracking/trackingsession/',
                    },
                    {
                        'title': 'SOS Incidents',
                        'icon': 'emergency',
                        'link': '/admin/emergency/emergencyincident/',
                    },
                    {
                        'title': 'Route Points',
                        'icon': 'location_on',
                        'link': '/admin/tracking/routepoint/',
                    },
                    {
                        'title': 'Devices',
                        'icon': 'smartphone',
                        'link': '/admin/devices/device/',
                    },
                ],
            },
            {
                'title': 'Access & Network',
                'separator': True,
                'items': [
                    {
                        'title': 'Users',
                        'icon': 'group',
                        'link': '/admin/accounts/user/',
                    },
                    {
                        'title': 'Trusted Contacts',
                        'icon': 'contact_phone',
                        'link': '/admin/contacts/trustedcontact/',
                    },
                    {
                        'title': 'Organizations',
                        'icon': 'business',
                        'link': '/admin/organizations/organization/',
                    },
                    {
                        'title': 'Developer API Keys',
                        'icon': 'key',
                        'link': '/admin/tracking/developerapikey/',
                    },
                ],
            },
            {
                'title': 'Platform',
                'separator': True,
                'items': [
                    {
                        'title': 'Geofences',
                        'icon': 'radar',
                        'link': '/admin/geofencing/geofence/',
                    },
                    {
                        'title': 'Notifications',
                        'icon': 'notifications',
                        'link': '/admin/notifications/notification/',
                    },
                    {
                        'title': 'Map Providers',
                        'icon': 'map',
                        'link': '/admin/maps/mapprovider/',
                    },
                    {
                        'title': 'Audit Logs',
                        'icon': 'fact_check',
                        'link': '/admin/audit/auditlog/',
                    },
                ],
            },
        ],
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'

CORS_ALLOW_ALL_ORIGINS = config(
    'CORS_ALLOW_ALL_ORIGINS', default=DEBUG, cast=bool
)
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in config('CORS_ALLOWED_ORIGINS', default='').split(',')
    if origin.strip()
]
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in config('CSRF_TRUSTED_ORIGINS', default='').split(',')
    if origin.strip()
]
if RAILWAY_PUBLIC_DOMAIN:
    railway_origin = f'https://{RAILWAY_PUBLIC_DOMAIN}'
    if railway_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(railway_origin)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = config(
    'SECURE_SSL_REDIRECT', default=not DEBUG, cast=bool
)
SECURE_HSTS_SECONDS = config(
    'SECURE_HSTS_SECONDS', default=3600 if not DEBUG else 0, cast=int
)
SECURE_REFERRER_POLICY = config(
    'SECURE_REFERRER_POLICY', default='strict-origin-when-cross-origin'
)
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'developer.authentication.ApiKeyAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
