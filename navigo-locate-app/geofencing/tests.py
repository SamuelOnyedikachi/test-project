from decimal import Decimal
from types import SimpleNamespace

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import Client, SimpleTestCase, TestCase, override_settings

from tracking.services import _point_is_inside_geofence

from .models import Geofence


class GeofenceBoundaryTests(SimpleTestCase):
    def test_rectangle_contains_point_inside_bounds(self):
        geofence = SimpleNamespace(
            shape_type=Geofence.ShapeType.RECTANGLE,
            north_latitude=Decimal("5.60"),
            south_latitude=Decimal("5.40"),
            east_longitude=Decimal("7.60"),
            west_longitude=Decimal("7.40"),
        )
        point = SimpleNamespace(latitude=Decimal("5.50"), longitude=Decimal("7.50"))
        self.assertTrue(_point_is_inside_geofence(geofence, point))

    def test_rectangle_rejects_point_outside_bounds(self):
        geofence = SimpleNamespace(
            shape_type=Geofence.ShapeType.SQUARE,
            north_latitude=Decimal("5.60"),
            south_latitude=Decimal("5.40"),
            east_longitude=Decimal("7.60"),
            west_longitude=Decimal("7.40"),
        )
        point = SimpleNamespace(latitude=Decimal("6.00"), longitude=Decimal("7.50"))
        self.assertFalse(_point_is_inside_geofence(geofence, point))

    def test_rectangle_requires_valid_bounds(self):
        geofence = Geofence(
            name="Invalid",
            shape_type=Geofence.ShapeType.RECTANGLE,
            center_latitude=5.5,
            center_longitude=7.5,
            radius_meters=100,
        )
        with self.assertRaises(ValidationError):
            geofence.clean()


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class GeofenceAdminMapTests(TestCase):
    def test_add_form_renders_boundary_map_editor(self):
        admin_user = get_user_model().objects.create_superuser(
            username="geofence-admin", email="admin@example.com", password="test-pass"
        )
        client = Client()
        client.force_login(admin_user)
        response = client.get("/admin/geofencing/geofence/add/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="geofence-map"')
        self.assertContains(response, 'data-shape="rectangle"')
