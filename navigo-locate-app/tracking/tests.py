import json

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.utils import timezone

from core.admin import navigo_admin_site
from organizations.models import Organization, OrganizationMember

from .access import sessions_visible_to
from .models import TrackingSession
from .services import record_location_update


class TrackingSessionAccessTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create_user(username="owner")
        self.viewer = User.objects.create_user(username="viewer")
        self.staff = User.objects.create_user(username="staff", is_staff=True)
        self.organization = Organization.objects.create(
            name="Response Agency",
            organization_type=Organization.OrganizationType.RESCUE,
        )
        self.session = TrackingSession.objects.create(user=self.owner)
        self.session.assigned_organizations.add(self.organization)

    def set_membership(self, role, *, is_active=True):
        OrganizationMember.objects.update_or_create(
            organization=self.organization,
            user=self.viewer,
            defaults={"role": role, "is_active": is_active},
        )

    def test_owner_and_staff_can_view_session(self):
        self.assertIn(self.session, sessions_visible_to(self.owner))
        self.assertIn(self.session, sessions_visible_to(self.staff))

    def test_operational_roles_can_view_assigned_session(self):
        for role in OrganizationMember.OPERATIONAL_ROLES:
            with self.subTest(role=role):
                self.set_membership(role)
                self.assertIn(self.session, sessions_visible_to(self.viewer))

    def test_member_cannot_view_assigned_session(self):
        self.set_membership(OrganizationMember.Role.MEMBER)
        self.assertNotIn(self.session, sessions_visible_to(self.viewer))

    def test_inactive_operational_member_cannot_view_session(self):
        self.set_membership(OrganizationMember.Role.RESPONDER, is_active=False)
        self.assertNotIn(self.session, sessions_visible_to(self.viewer))

    def test_operational_role_cannot_view_unassigned_session(self):
        self.set_membership(OrganizationMember.Role.RESPONDER)
        self.session.assigned_organizations.clear()
        self.assertNotIn(self.session, sessions_visible_to(self.viewer))


class LiveOperationsDataTests(TestCase):
    def test_recorded_location_is_returned_to_admin_follow_map(self):
        user = get_user_model().objects.create_user(
            username="tracked-user",
            full_name="Tracked User",
        )
        session = TrackingSession.objects.create(user=user)
        record_location_update(
            session,
            {
                "latitude": "6.5244000",
                "longitude": "3.3792000",
                "accuracy": 8.0,
                "speed": 1.5,
                "heading": 90.0,
                "recorded_at": timezone.now(),
            },
            actor=user,
        )

        response = navigo_admin_site.live_tracking_data(
            RequestFactory().get("/admin/operations/live-tracking/data/")
        )
        payload = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(payload["sessions"]), 1)
        self.assertEqual(payload["sessions"][0]["id"], session.id)
        self.assertEqual(payload["sessions"][0]["latitude"], 6.5244)
        self.assertEqual(payload["sessions"][0]["longitude"], 3.3792)
