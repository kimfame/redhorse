import logging

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user_profile.models import Profile
from core.utils import get_client_with_login_status
from scripts import base_data_generator
from user_profile.factories import ProfileFactory

logger = logging.getLogger(__name__)


class CreateProfileTestCase(APITestCase):
    def setUp(self):
        base_data_generator.run()
        self.client = get_client_with_login_status(self.client)
        self.url = reverse("my_profile")
        profile = ProfileFactory.build()
        self.data = {
            "nickname": profile.nickname,
            "birthdate": profile.birthdate.strftime("%Y-%m-%d"),
            "gender": profile.gender,
            "preferred_gender": profile.preferred_gender,
            "mbti": profile.mbti,
            "passions": profile.passions,
            "height": profile.height,
            "religion": profile.religion,
            "smoking_status": profile.smoking_status,
            "drinking_status": profile.drinking_status,
            "location": profile.location,
            "bio": profile.bio,
        }

    def test_can_create_profile(self):
        response = self.client.post(self.url, self.data)
        logger.info(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateProfileTestCase(APITestCase):
    def setUp(self):
        base_data_generator.run()
        self.profile = ProfileFactory()
        self.client = get_client_with_login_status(self.client, self.profile.user)
        self.url = reverse("my_profile")

    def test_can_update_profile(self):
        new_profile = ProfileFactory.build()
        data = {
            "nickname": new_profile.nickname,
            "birthdate": new_profile.birthdate.strftime("%Y-%m-%d"),
            "gender": new_profile.gender,
            "preferred_gender": new_profile.preferred_gender,
            "mbti": new_profile.mbti,
            "passions": new_profile.passions,
            "height": new_profile.height,
            "religion": new_profile.religion,
            "smoking_status": new_profile.smoking_status,
            "drinking_status": new_profile.drinking_status,
            "location": new_profile.location,
            "bio": new_profile.bio,
        }
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["nickname"], data["nickname"])
        self.assertEqual(response.data["height"], data["height"])
        self.assertEqual(response.data["location"], data["location"])
        self.assertEqual(response.data["bio"], data["bio"])

        updated_profile = Profile.objects.filter(id=self.profile.id).first()
        self.assertEqual(updated_profile.birthdate, self.profile.birthdate)
        self.assertEqual(updated_profile.gender, self.profile.gender)


class ReadProfileTestCase(APITestCase):
    def setUp(self):
        base_data_generator.run()
        self.profile = ProfileFactory()
        self.client = get_client_with_login_status(self.client, self.profile.user)

    def test_can_get_my_profile(self):
        url = reverse("my_profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_get_opposite_profile(self):
        new_profile = ProfileFactory()
        url = reverse("opposite_profile", kwargs={"uuid": new_profile.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileOptionTestCase(APITestCase):
    def setUp(self):
        base_data_generator.run()
        self.client = get_client_with_login_status(self.client)

    def test_can_get_option_list(self):
        option_field_names = [
            "genders",
            "preferred-genders",
            "mbti-types",
            "drinking-status",
            "religions",
            "locations",
            "passions",
        ]

        for field_name in option_field_names:
            url = reverse("option_list", kwargs={"option_field_name": field_name})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data)
