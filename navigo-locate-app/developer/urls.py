from django.urls import path

from .views import DeveloperApiKeyDetailView, DeveloperApiKeyListCreateView

urlpatterns = [
    path("api-keys/", DeveloperApiKeyListCreateView.as_view(), name="developer-api-keys"),
    path("api-keys/<int:pk>/", DeveloperApiKeyDetailView.as_view(), name="developer-api-key-detail"),
]
