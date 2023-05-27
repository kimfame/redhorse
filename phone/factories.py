import random
import factory

from factory.django import DjangoModelFactory

from core.utils import get_random_verification_code
from phone.models import PhoneVerificationHistory, UserPhone
from user.factories import UserFactory


def get_random_phone_number() -> str:
    return f"010{random.randint(0,99999999):08}"


class PhoneVerificationHistoryFactory(DjangoModelFactory):
    class Meta:
        model = PhoneVerificationHistory

    phone_number = get_random_phone_number()
    verification_code = get_random_verification_code()


class UserPhoneFactory(DjangoModelFactory):
    class Meta:
        model = UserPhone

    user = factory.SubFactory(UserFactory)
    phone_number = get_random_phone_number()
