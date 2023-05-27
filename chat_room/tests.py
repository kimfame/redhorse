from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.test import get_client_with_login_status
from chat_room.factories import ChatRoomFactory
from chat_room.models import ChatRoomMember, ChatRoom
from match.factories import MatchFactory
from scripts import base_data_generator
from user_profile.tests import ProfileFactory


class ChatRoomTestCase(APITestCase):
    def setUp(self):
        base_data_generator.run()
        self.profile = ProfileFactory()
        self.client = get_client_with_login_status(self.client, self.profile.user)

    def test_can_create_chat_room(self):
        url = reverse("match_create")

        opposite_profile = ProfileFactory()
        MatchFactory(
            sender=opposite_profile.user,
            receiver=self.profile.user,
            is_liked=True,
        )

        data = {"uuid": opposite_profile.uuid, "is_liked": True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        chat_room = (
            ChatRoom.objects.filter(
                users__in=[opposite_profile.user, self.profile.user]
            )
            .distinct()
            .exists()
        )

        self.assertTrue(chat_room)

    def test_can_get_chat_room_list(self):
        url = reverse("chat_room_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_leave_chat_room(self):
        room = ChatRoomFactory(users=[self.profile.user])

        url = reverse("chat_room_leave", kwargs={"uuid": room.uuid})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        member = ChatRoomMember.objects.filter(
            room=room, user=self.profile.user
        ).first()
        self.assertFalse(member.is_active)

    def test_can_retrieve_chat_room(self):
        room = ChatRoomFactory(users=[self.profile.user])

        url = reverse("chat_room_detail", kwargs={"uuid": room.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
