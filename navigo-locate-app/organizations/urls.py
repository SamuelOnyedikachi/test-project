from django.urls import path

from .views import (
    OrganizationDetailView,
    OrganizationListCreateView,
    OrganizationMemberListCreateView,
)

urlpatterns = [
    path("", OrganizationListCreateView.as_view(), name="organizations"),
    path("<int:pk>/", OrganizationDetailView.as_view(), name="organization-detail"),
    path("members/", OrganizationMemberListCreateView.as_view(), name="organization-members"),
]
