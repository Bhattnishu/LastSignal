from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import ItemReport, RecoveryRequest

User = get_user_model()


class RecoveryRequestTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.customer = User.objects.create_user(
            email="customer@test.com",
            name="Customer",
            phone="9876543210",
            password="testpass123"
        )

        self.provider = User.objects.create_user(
            email="provider@test.com",
            name="Provider",
            phone="9876543211",
            password="testpass123"
        )

        self.lost_report = ItemReport.objects.create(
            user=self.customer,
            report_type="LOST",
            item_name="Black Backpack",
            category="BAGS",
            description="Black backpack",
            location="Library",
            city="Pithoragarh"
        )

        self.found_report = ItemReport.objects.create(
            user=self.provider,
            report_type="FOUND",
            item_name="Black Backpack",
            category="BAGS",
            description="Found black backpack",
            location="Library",
            city="Pithoragarh"
        )

        self.recovery_request = RecoveryRequest.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            requester=self.customer,
            message="I think this is my backpack."
        )

    def test_only_found_report_owner_can_respond(self):
        self.client.force_authenticate(user=self.customer)

        response = self.client.patch(
            f"/api/items/recovery-requests/{self.recovery_request.id}/respond/",
            {"status": "ACCEPTED"},
            format="json"
        )

        self.assertEqual(response.status_code, 404)

    def test_found_report_owner_can_accept_request(self):
        self.client.force_authenticate(user=self.provider)

        response = self.client.patch(
            f"/api/items/recovery-requests/{self.recovery_request.id}/respond/",
            {"status": "ACCEPTED"},
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.recovery_request.refresh_from_db()
        self.assertEqual(self.recovery_request.status, "ACCEPTED")

    def test_response_cannot_change_other_fields(self):
        self.client.force_authenticate(user=self.provider)

        response = self.client.patch(
            f"/api/items/recovery-requests/{self.recovery_request.id}/respond/",
            {
                "status": "ACCEPTED",
                "message": "Changed message"
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.recovery_request.refresh_from_db()
        self.assertEqual(
            self.recovery_request.message,
            "I think this is my backpack."
        )
