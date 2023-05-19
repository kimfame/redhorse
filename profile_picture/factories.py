import factory

from factory.django import DjangoModelFactory

from profile_picture.models import ProfilePicture
from user.factories import UserFactory


class ProfilePictureFactory(DjangoModelFactory):
    class Meta:
        model = ProfilePicture

    user = factory.SubFactory(UserFactory)
    image = factory.django.ImageField(color="black")
