import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from faker import Faker

from phone.factories import PhoneVerificationHistoryFactory, UserPhoneFactory
from user.factories import UserFactory

fake = Faker()


class CreateUserTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("create_user")
        self.phone_verification_history = PhoneVerificationHistoryFactory(
            is_verified=True
        )
        self.password = fake.password()

    def test_can_create_user(self):
        user = UserFactory.build(password=self.password)
        response = self.client.post(
            self.url,
            {
                "username": user.username,
                "password": self.password,
                "uuid": str(self.phone_verification_history.uuid),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_not_create_user(self):
        user = UserFactory.build(password=self.password)
        response = self.client.post(
            self.url,
            {
                "username": user.username,
                "password": user.password,
                "uuid": str(uuid.uuid4()),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeactivateUserTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("delete_user")
        self.user = UserFactory()

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_can_deactivate_user(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ChangePasswordTestCase(APITestCase):
    def setUp(self):
        self.password = fake.password()
        self.user = UserFactory(password=self.password)

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_can_change_password(self):
        new_password = fake.password()
        change_password_response = self.client.patch(
            reverse("change_password"),
            {
                "old_password": self.password,
                "password": new_password,
            },
        )
        self.assertEqual(
            change_password_response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        login_response = self.client.post(
            reverse("token_obtain_pair"),
            {
                "username": self.user.username,
                "password": new_password,
            },
        )
        self.assertEqual(
            login_response.status_code,
            status.HTTP_200_OK,
        )


class ResetPassword(APITestCase):
    def setUp(self):
        self.url = reverse("reset_password")
        self.user_phone = UserPhoneFactory()

    def test_can_reset_password(self):
        response = self.client.post(
            self.url,
            {
                "phone_number": self.user_phone.phone_number,
                "username": self.user_phone.user.username,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
