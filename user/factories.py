import factory
import string

from django.contrib.auth.models import User
from faker import Faker
from factory.django import DjangoModelFactory
from secrets import choice

fake = Faker()


def get_random_username(len: int) -> str:
    return "".join(
        [choice(string.ascii_lowercase + string.digits + "-_") for _ in range(len)]
    )


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.sequence(lambda n: f"user_{n+2}")
    password = factory.PostGenerationMethodCall("set_password", fake.password())
