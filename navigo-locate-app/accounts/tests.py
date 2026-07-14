from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from rest_framework.test import APITestCase

from .models import PasswordResetOTP


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    PASSWORD_RESET_OTP_MINUTES=10,
)
class PasswordResetApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="psalmcodes",
            email="samuel@example.com",
            password="OldPassword1225",
        )

    def test_login_response_contains_authenticated_username(self):
        response = self.client.post(
            "/api/v1/auth/login/",
            {"username": "psalmcodes", "password": "OldPassword1225"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user"]["username"], "psalmcodes")

    def test_request_sends_six_digit_code_without_storing_plaintext(self):
        response = self.client.post(
            "/api/v1/auth/password-reset/request/",
            {"email": self.user.email},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        code = self._code_from_email()
        self.assertRegex(code, r"^\d{6}$")
        self.assertNotEqual(PasswordResetOTP.objects.get().code_hash, code)

    def test_unknown_email_returns_same_generic_response(self):
        response = self.client.post(
            "/api/v1/auth/password-reset/request/",
            {"email": "unknown@example.com"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("If an active account", response.data["detail"])
        self.assertEqual(len(mail.outbox), 0)

    def test_valid_code_resets_password_and_cannot_be_reused(self):
        self.client.post(
            "/api/v1/auth/password-reset/request/",
            {"email": self.user.email},
            format="json",
        )
        payload = {
            "email": self.user.email,
            "otp": self._code_from_email(),
            "new_password": "NewSecurePassword1225",
            "confirm_password": "NewSecurePassword1225",
        }
        response = self.client.post(
            "/api/v1/auth/password-reset/confirm/", payload, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewSecurePassword1225"))
        self.assertEqual(
            self.client.post(
                "/api/v1/auth/password-reset/confirm/", payload, format="json"
            ).status_code,
            400,
        )

    def test_five_wrong_attempts_invalidate_code(self):
        self.client.post(
            "/api/v1/auth/password-reset/request/",
            {"email": self.user.email},
            format="json",
        )
        valid_code = self._code_from_email()
        wrong_code = "000000" if valid_code != "000000" else "999999"
        for _ in range(5):
            response = self.client.post(
                "/api/v1/auth/password-reset/confirm/",
                {
                    "email": self.user.email,
                    "otp": wrong_code,
                    "new_password": "NewSecurePassword1225",
                    "confirm_password": "NewSecurePassword1225",
                },
                format="json",
            )
            self.assertEqual(response.status_code, 400)
        otp = PasswordResetOTP.objects.get()
        self.assertEqual(otp.attempts, 5)
        self.assertIsNotNone(otp.consumed_at)

    def _code_from_email(self):
        return mail.outbox[-1].body.split("code is: ", 1)[1].splitlines()[0]
