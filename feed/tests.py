from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.test import get_client_with_login_status
from core.utils import get_remaining_like_num
from scripts import base_data_generator
from user_profile.factories import ProfileFactory


class FeedTestCase(APITestCase):
    def setUp(self):
        base_data_generator.run()
        self.profile = ProfileFactory()
        self.client = get_client_with_login_status(self.client, self.profile.user)
        self.url = reverse("feed")
        ProfileFactory.create_batch(size=2, gender="M")
        ProfileFactory.create_batch(size=2, gender="F")

    def test_can_get_gender_M_or_F_profiles(self):
        for preferred_gender in ["M", "F"]:
            self.profile.preferred_gender = preferred_gender
            self.profile.save()

            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            for ordered_dict_profile in response.data:
                profile = dict(ordered_dict_profile.items())
                self.assertEqual(profile["gender"], preferred_gender)

    def test_can_get_gender_M_and_F_profiles(self):
        feed_profile_num = get_remaining_like_num(self.profile.user)

        if feed_profile_num >= 4:
            self.profile.preferred_gender = "A"
            self.profile.save()

            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            gender_counter = {"M": 0, "F": 0}

            for ordered_dict_profile in response.data:
                profile = dict(ordered_dict_profile.items())
                gender_counter[f'{profile["gender"]}'] += 1

            self.assertEqual(gender_counter["M"], 2)
            self.assertEqual(gender_counter["F"], 2)
