from django.contrib.auth import get_user_model
from django.contrib import admin
from django.test import RequestFactory
from django.test import TestCase
from rest_framework.test import APIClient

from .forms import NotificationAdminForm
from .admin import NotificationAdmin
from .models import Notification


class NotificationAudienceTests(TestCase):
    def setUp(self):
        self.first = get_user_model().objects.create_user(username="first", password="test-pass")
        self.second = get_user_model().objects.create_user(username="second", password="test-pass")

    def test_all_audience_returns_every_active_user(self):
        form = NotificationAdminForm(
            data={
                "audience": "all",
                "channel": Notification.Channel.PUSH,
                "status": Notification.Status.PENDING,
                "scope": Notification.Scope.SAFETY,
                "title": "Weather warning",
                "message": "Take care on the road.",
                "show_as_popup": True,
                "payload": "{}",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual({user.pk for user in form.recipients()}, {self.first.pk, self.second.pk})

    def test_admin_creates_a_notification_for_every_selected_audience_user(self):
        form = NotificationAdminForm(
            data={
                "audience": "all",
                "channel": Notification.Channel.PUSH,
                "status": Notification.Status.PENDING,
                "scope": Notification.Scope.SYSTEM,
                "title": "Platform notice",
                "message": "Navigo maintenance is complete.",
                "show_as_popup": True,
                "payload": "{}",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        notification_admin = NotificationAdmin(Notification, admin.site)
        notification_admin.save_model(
            RequestFactory().post("/admin/notifications/notification/add/"),
            form.save(commit=False),
            form,
            change=False,
        )
        self.assertEqual(Notification.objects.count(), 2)
        self.assertEqual(set(Notification.objects.values_list("provider", flat=True)), {"in_app"})

    def test_user_can_mark_own_notification_read(self):
        notification = Notification.objects.create(
            user=self.first,
            channel=Notification.Channel.PUSH,
            title="Check in",
            message="Please confirm you are safe.",
        )
        client = APIClient()
        client.force_authenticate(self.first)
        response = client.patch(f"/api/v1/notifications/{notification.pk}/", {}, format="json")
        self.assertEqual(response.status_code, 200)
        notification.refresh_from_db()
        self.assertIsNotNone(notification.read_at)

    def test_user_cannot_read_another_users_notification(self):
        notification = Notification.objects.create(
            user=self.second,
            channel=Notification.Channel.PUSH,
            title="Private",
            message="For one user.",
        )
        client = APIClient()
        client.force_authenticate(self.first)
        self.assertEqual(client.get(f"/api/v1/notifications/{notification.pk}/").status_code, 404)
