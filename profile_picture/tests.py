from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from PIL import Image

from core.test import get_client_with_login_status
from profile_picture.factories import ProfilePictureFactory
from scripts import base_data_generator
from user_profile.tests import ProfileFactory


class ProfilePictureTestCase(APITestCase):
    def _create_temporary_image(self):
        stream_image = BytesIO()
        image = Image.new("RGB", (100, 100), "black")
        image.save(stream_image, format="JPEG")
        stream_image.seek(0)
        return SimpleUploadedFile("black_square.jpg", stream_image.getvalue())

    def setUp(self):
        base_data_generator.run()
        self.profile = ProfileFactory()
        self.client = get_client_with_login_status(self.client, self.profile.user)

    def test_can_create_profile_picture(self):
        url = reverse("profile_picture_list")
        new_image = self._create_temporary_image()

        response = self.client.post(url, {"image": new_image}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_change_main_profile_picture(self):
        profile_picture_list = ProfilePictureFactory.create_batch(
            size=3, user=self.profile.user
        )
        for profile_picture in profile_picture_list:
            url = reverse(
                "profile_picture_detail",
                kwargs={"uuid": profile_picture.uuid},
            )

            response = self.client.patch(url, {"main": True})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["main"], True)


class ProfilePictureTestCase(APITestCase):
    def setUp(self):
        base_data_generator.run()
        self.profile = ProfileFactory()
        self.client = get_client_with_login_status(self.client, self.profile.user)

    def test_can_delete_profile_picture(self):
        profile_picture_list = ProfilePictureFactory.create_batch(
            size=2, user=self.profile.user
        )
        url = reverse(
            "profile_picture_detail",
            kwargs={"uuid": profile_picture_list[0].uuid},
        )

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_change_main_profile_picture_by_delete_method(self):
        profile_picture_list = ProfilePictureFactory.create_batch(
            size=2, user=self.profile.user
        )

        profile_picture_list[0].main = True
        profile_picture_list[0].save()

        url = reverse(
            "profile_picture_detail",
            kwargs={"uuid": profile_picture_list[0].uuid},
        )

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        profile_picture_list[1].refresh_from_db()
        self.assertEqual(profile_picture_list[1].main, True)

    def test_can_not_delete_last_profile_picture(self):
        profile_picture = ProfilePictureFactory.create(user=self.profile.user)

        url = reverse(
            "profile_picture_detail",
            kwargs={"uuid": profile_picture.uuid},
        )

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
