from django.urls import path

from .views import DeviceDetailView, DeviceListCreateView, DeviceRegisterView

urlpatterns = [
    path("register/", DeviceRegisterView.as_view(), name="device-register"),
    path("", DeviceListCreateView.as_view(), name="devices"),
    path("<int:pk>/", DeviceDetailView.as_view(), name="device-detail"),
]
