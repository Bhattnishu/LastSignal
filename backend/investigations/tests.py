from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from items.models import ItemReport
from .models import Investigation

User = get_user_model()


class InvestigationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="user@test.com",
            name="Test User",
            phone="9876543210",
            password="testpass123"
        )

        self.other_user = User.objects.create_user(
            email="other@test.com",
            name="Other User",
            phone="9876543211",
            password="testpass123"
        )

        self.lost_report = ItemReport.objects.create(
            user=self.user,
            report_type="LOST",
            item_name="Black Backpack",
            category="BAGS",
            description="Black backpack",
            location="Library",
            city="Pithoragarh"
        )

        self.client.force_authenticate(user=self.user)

    def test_user_can_create_own_investigation(self):
        response = self.client.post(
            "/api/investigations/",
            {"lost_report": self.lost_report.id},
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Investigation.objects.filter(
                lost_report=self.lost_report
            ).exists()
        )

    def test_user_cannot_investigate_other_users_report(self):
        other_report = ItemReport.objects.create(
            user=self.other_user,
            report_type="LOST",
            item_name="Blue Wallet",
            category="ACCESSORIES",
            description="Blue wallet",
            location="Bus Stand",
            city="Pithoragarh"
        )

        response = self.client.post(
            "/api/investigations/",
            {"lost_report": other_report.id},
            format="json"
        )

        self.assertEqual(response.status_code, 404)

    def test_duplicate_investigation_is_rejected(self):
        Investigation.objects.create(
            lost_report=self.lost_report,
            user=self.user
        )

        response = self.client.post(
            "/api/investigations/",
            {"lost_report": self.lost_report.id},
            format="json"
        )

        self.assertEqual(response.status_code, 400)
