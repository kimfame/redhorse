from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.utils import get_client_with_login_status, get_remaining_like_num
from scripts import base_data_generator
from user_profile.factories import ProfileFactory


class FeedTestCase(APITestCase):
    def setUp(self):
        base_data_generator.run()
        self.url = reverse("feed")

    def test_can_get_gender_M_or_F_profiles(self):
        my_profile = ProfileFactory(preferred_gender="M")
        self.client = get_client_with_login_status(self.client, my_profile.user)

        for gender in ["M", "F"]:
            ProfileFactory.create_batch(size=2, gender=gender)

        for preferred_gender in ["M", "F"]:
            if my_profile.preferred_gender != preferred_gender:
                my_profile.preferred_gender = preferred_gender
                my_profile.save()

            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            for ordered_dict_profile in response.data:
                profile = dict(ordered_dict_profile.items())
                self.assertEqual(profile["gender"], preferred_gender)

    def test_can_get_gender_M_and_F_profiles(self):
        my_profile = ProfileFactory(preferred_gender="A")
        self.client = get_client_with_login_status(self.client, my_profile.user)

        feed_profile_num = get_remaining_like_num(my_profile.user)
        self.assertGreaterEqual(feed_profile_num, 4)

        for gender in ["M", "F"]:
            ProfileFactory.create_batch(size=2, gender=gender)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        gender_counter = {"M": 0, "F": 0}

        for ordered_dict_profile in response.data:
            profile = dict(ordered_dict_profile.items())
            gender_counter[f'{profile["gender"]}'] += 1

        self.assertEqual(gender_counter["M"], 2)
        self.assertEqual(gender_counter["F"], 2)

    def test_can_exclude_inactive_users(self):
        my_profile = ProfileFactory(preferred_gender="F")
        self.client = get_client_with_login_status(self.client, my_profile.user)

        feed_profile_num = get_remaining_like_num(my_profile.user)
        self.assertGreaterEqual(feed_profile_num, 2)

        ProfileFactory(gender="F")
        ProfileFactory(gender="F", user__is_active=False)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
