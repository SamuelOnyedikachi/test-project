from django.urls import path

from .views import MapProviderListView

urlpatterns = [
    path("providers/", MapProviderListView.as_view(), name="map-providers"),
]
