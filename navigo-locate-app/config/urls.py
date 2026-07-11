from django.http import JsonResponse
from django.urls import include, path

from core.admin import navigo_admin_site


def health_check(_request):
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('admin/', navigo_admin_site.urls),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/devices/', include('devices.urls')),
    path('api/v1/tracking/', include('tracking.urls')),
    path('api/v1/emergency/', include('emergency.urls')),
    path('api/v1/contacts/', include('contacts.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
    path('api/v1/maps/', include('maps.urls')),
    path('api/v1/geofences/', include('geofencing.urls')),
    path('api/v1/organizations/', include('organizations.urls')),
    path('api/v1/developer/', include('developer.urls')),
    path('api/v1/audit/', include('audit.urls')),
]
