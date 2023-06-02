import factory
import factory.fuzzy
import random

from factory.django import DjangoModelFactory
from faker import Faker

from core.utils import get_option_code_list, get_random_adult_birthdate
from user.factories import UserFactory
from user_profile import choices
from user_profile.models import Profile

fake = Faker()


PROFILE_OPTION_VALUES = {
    "gender": [c[0] for c in choices.Gender.choices],
    "preferred_gender": [c[0] for c in choices.PreferredGender.choices],
    "mbti": get_option_code_list("mbti"),
    "religion": [c[0] for c in choices.Religion.choices],
    "drinking_status": [c[0] for c in choices.DrinkingStatus.choices],
    "location": [c[0] for c in choices.Location.choices],
    "passion": get_option_code_list("passion"),
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
    passions = factory.lazy_attribute(
        lambda o: random.sample(PROFILE_OPTION_VALUES["passion"], random.randint(1, 3))
    )
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
