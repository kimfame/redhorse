import factory
import string

from secrets import choice

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from faker import Faker

fake = Faker()


def get_random_username(len: int) -> str:
    return "".join(
        [choice(string.ascii_lowercase + string.digits + "-_") for _ in range(len)]
    )


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.sequence(lambda n: f"user_{n+2}")
    password = factory.lazy_attribute(lambda o: make_password(o.username))
