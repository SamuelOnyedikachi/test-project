from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class ReverseGeocodeApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="mapper", password="test-pass")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    @patch("maps.views.reverse_geocode")
    def test_returns_structured_address(self, reverse_geocode):
        reverse_geocode.return_value = {
            "formatted_address": "Ikot Ekpene Road, Umuahia, Abia, Nigeria",
            "street": "Ikot Ekpene Road",
            "lga": "Umuahia North",
            "state": "Abia",
        }
        response = self.client.get(
            "/api/v1/maps/reverse-geocode/?latitude=5.5249&longitude=7.4946"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["lga"], "Umuahia North")

    def test_rejects_invalid_coordinates(self):
        response = self.client.get(
            "/api/v1/maps/reverse-geocode/?latitude=200&longitude=7.4"
        )
        self.assertEqual(response.status_code, 400)
