import random

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.test import get_client_with_login_status
from scripts import base_data_generator
from user_profile.factories import ProfileFactory, PROFILE_OPTION_VALUES


class CreateProfileTestCase(APITestCase):
    def setUp(self):
        base_data_generator.run()
        self.client = get_client_with_login_status()
        self.url = reverse("my_profile")
        profile = ProfileFactory.build()
        self.data = {
            "nickname": profile.nickname,
            "birthdate": profile.birthdate.strftime("%Y-%m-%d"),
            "gender": profile.gender,
            "preferred_gender": profile.preferred_gender,
            "mbti": profile.mbti,
            "passions": random.sample(
                PROFILE_OPTION_VALUES["passion"], settings.MAX_PASSION_NUM
            ),
            "height": profile.height,
            "religion": profile.religion,
            "smoking_status": profile.smoking_status,
            "drinking_status": profile.drinking_status,
            "location": profile.location,
            "bio": profile.bio,
        }

    def test_can_create_profile(self):
        response = self.client.post(self.url, self.data)
        if response.status_code != 201:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
