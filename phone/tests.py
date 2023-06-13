import random

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from phone.factories import PhoneVerificationHistoryFactory


class CreatePhoneVerificationHistoryTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("send_code-list")

    def test_can_not_create_phone_verification_history(self):
        response = self.client.post(
            self.url,
            {"phone_number": str(random.randint(0, 999999999999))},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_create_phone_verification_history(self):
        response = self.client.post(
            self.url,
            {"phone_number": PhoneVerificationHistoryFactory.stub().phone_number},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdatePhoneVerificationHistoryTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("verify_code-list")
        self.verification_history = PhoneVerificationHistoryFactory()

    def test_can_not_verify_code(self):
        response = self.client.post(
            self.url,
            {
                "phone_number": self.verification_history.phone_number,
                "verification_code": f"{random.randint(0, 99999):06}",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_verify_code(self):
        response = self.client.post(
            self.url,
            {
                "phone_number": self.verification_history.phone_number,
                "verification_code": self.verification_history.verification_code,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
