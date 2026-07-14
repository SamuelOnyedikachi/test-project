from django.urls import path

from .views import MapProviderListView, ReverseGeocodeView

urlpatterns = [
    path("providers/", MapProviderListView.as_view(), name="map-providers"),
    path("reverse-geocode/", ReverseGeocodeView.as_view(), name="reverse-geocode"),
]
