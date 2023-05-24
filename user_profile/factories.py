import factory
import factory.fuzzy
import random

from django.conf import settings
from factory.django import DjangoModelFactory
from faker import Faker

from core.test import get_random_adult_birthdate
from core.utils import get_option_code_list
from user.factories import UserFactory
from user_profile.models import Profile
from passion.models import Passion

fake = Faker()


PROFILE_OPTION_VALUES = {
    "gender": get_option_code_list("gender"),
    "preferred_gender": get_option_code_list("preferred_gender"),
    "mbti": get_option_code_list("mbti"),
    "religion": get_option_code_list("religion"),
    "drinking_status": get_option_code_list("drinking_status"),
    "location": get_option_code_list("location"),
    "passion": list(Passion.objects.all().values_list("id", flat=True)),
}


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    nickname = factory.sequence(lambda n: f"nickname_{n+2}")
    birthdate = factory.fuzzy.FuzzyDate(*get_random_adult_birthdate())
    gender = factory.fuzzy.FuzzyChoice(choices=PROFILE_OPTION_VALUES["gender"])
    preferred_gender = factory.fuzzy.FuzzyChoice(
        choices=PROFILE_OPTION_VALUES["preferred_gender"]
    )
    mbti = factory.fuzzy.FuzzyChoice(choices=PROFILE_OPTION_VALUES["mbti"])
    height = factory.lazy_attribute(lambda o: str(random.randint(100, 299)))
    religion = factory.fuzzy.FuzzyChoice(choices=PROFILE_OPTION_VALUES["religion"])
    smoking_status = factory.fuzzy.FuzzyChoice(choices=[True, False])
    drinking_status = factory.fuzzy.FuzzyChoice(
        choices=PROFILE_OPTION_VALUES["drinking_status"]
    )
    location = factory.fuzzy.FuzzyChoice(choices=PROFILE_OPTION_VALUES["location"])
    bio = factory.lazy_attribute(
        lambda o: fake.paragraph(nb_sentences=2, variable_nb_sentences=False)
    )

    @factory.post_generation
    def passions(self, create, extracted, **kwargs):
        if extracted:
            for passion in extracted:
                self.passions.add(passion)
            return

        if create:
            self.passions.set(
                random.sample(
                    PROFILE_OPTION_VALUES["passion"], settings.MAX_PASSION_NUM
                )
            )
