from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker

from chat_room.factories import ChatRoomFactory
from chat_message.factories import ChatMessageFactory
from core.utils import get_client_with_login_status
from scripts import base_data_generator
from user_profile.tests import ProfileFactory

fake = Faker()


class ChatMessageTestCase(APITestCase):
    def setUp(self):
        base_data_generator.run()
        self.profile = ProfileFactory()
        self.client = get_client_with_login_status(self.client, self.profile.user)

    def test_can_get_message_list(self):
        room = ChatRoomFactory(users=[self.profile.user])
        ChatMessageFactory.create_batch(size=10, room=room, user=self.profile.user)

        url = reverse("chat_message_list", kwargs={"uuid": room.uuid})
        response = self.client.get(url)

        message_list = dict(response.data.items())["results"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(message_list), 10)

    def test_can_create_message(self):
        room = ChatRoomFactory(users=[self.profile.user])

        url = reverse("chat_message_create", kwargs={"uuid": room.uuid})
        response = self.client.post(
            url,
            {"message": fake.paragraph(nb_sentences=3, variable_nb_sentences=False)},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
