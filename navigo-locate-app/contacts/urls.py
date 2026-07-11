from django.urls import path

from .views import TrustedContactDetailView, TrustedContactListCreateView

urlpatterns = [
    path("", TrustedContactListCreateView.as_view(), name="trusted-contacts"),
    path("<int:pk>/", TrustedContactDetailView.as_view(), name="trusted-contact-detail"),
]
