from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.test import get_client_with_login_status
from core.utils import get_remaining_like_num
from match.factories import MatchFactory
from scripts import base_data_generator
from user_profile.tests import ProfileFactory


class CreateMatchTestCase(APITestCase):
    def setUp(self):
        base_data_generator.run()
        self.profile = ProfileFactory()
        self.client = get_client_with_login_status(self.client, self.profile.user)
        self.url = reverse("match_create")

    def test_can_create_match(self):
        target_profile = ProfileFactory()
        data = {"uuid": target_profile.uuid, "is_liked": True}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_not_create_same_match_to_same_user(self):
        target_profile = ProfileFactory()
        MatchFactory(sender=self.profile.user, receiver=target_profile.user)

        data = {"uuid": target_profile.uuid, "is_liked": True}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_not_create_match_by_limit_of_like_num(self):
        like_num = get_remaining_like_num(self.profile.user)
        MatchFactory.create_batch(size=like_num, sender=self.profile.user)

        profile = ProfileFactory()
        data = {"uuid": profile.uuid, "is_liked": True}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReceivedLikeTestCase(APITestCase):
    def setUp(self):
        base_data_generator.run()
        self.url = reverse("match_received_likes")

    def test_can_get_profiles_who_like_me(self):
        my_profile = ProfileFactory()
        self.client = get_client_with_login_status(self.client, my_profile.user)

        opposite_profile = ProfileFactory()
        MatchFactory(
            sender=opposite_profile.user,
            receiver=my_profile.user,
            is_liked=True,
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_can_exclude_inactive_users(self):
        my_profile = ProfileFactory(preferred_gender="F")
        self.client = get_client_with_login_status(self.client, my_profile.user)

        feed_profile_num = get_remaining_like_num(my_profile.user)
        self.assertGreaterEqual(feed_profile_num, 2)

        for is_active in range(2):
            opposite_profile = ProfileFactory(gender="F", user__is_active=is_active)
            MatchFactory(
                sender=opposite_profile.user,
                receiver=my_profile.user,
                is_liked=True,
            )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class RemainingLikeTestCase(APITestCase):
    def setUp(self):
        base_data_generator.run()
        self.profile = ProfileFactory()
        self.client = get_client_with_login_status(self.client, self.profile.user)
        self.url = reverse("remaining_like_num")

    def test_can_get_remaining_like_num(self):
        like_num = get_remaining_like_num(self.profile.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["like_num"], like_num)

    def test_can_count_remaining_like_num(self):
        init_like_num = get_remaining_like_num(self.profile.user)

        profile = ProfileFactory()
        data = {"uuid": profile.uuid, "is_liked": True}
        self.client.post(reverse("match_create"), data)

        response = self.client.get(self.url)
        self.assertEqual(response.data["like_num"], init_like_num - 1)
