import logging
import random

from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import OperationalError

from core.utils import get_random_string, get_common_code_list
from user_profile.models import Profile
from passion.models import Passion

logger = logging.getLogger(__name__)


def run():
    create_superuser()
    create_test_users()


def create_superuser():
    logger.info("Create superuser")
    try:
        if User.objects.filter(is_superuser=True).exists():
            logger.info("Superuser already exist")
            return

        User.objects.create_superuser(
            "admin@test.com", "admin@test.com", "admin@test.com"
        )
    except OperationalError as e:
        logger.debug(e, exc_info=True)


def get_passion_list() -> list:
    return list(Passion.objects.all().values_list("id", flat=True))


def get_random_date() -> date:
    today = date.today()
    start_date = date(today.year - 70, 1, 1)

    return start_date + timedelta(days=random.randint(1, 365 * 50))


def create_test_users(user_num=10):
    logger.info("Create fake users")

    choice_field = {
        "gender": get_common_code_list("gender"),
        "preferred_gender": get_common_code_list("preferred_gender"),
        "mbti": get_common_code_list("mbti"),
        "religion": get_common_code_list("religion"),
        "drinking_status": get_common_code_list("drinking_status"),
        "location": get_common_code_list("location"),
        "passion": get_passion_list(),
    }

    user_list = []
    for i in range(user_num):
        username = f"test_{i}"
        user = User(username=username)
        user.set_password(username)
        user_list.append(user)

    users = User.objects.bulk_create(user_list)

    for user in users:
        profile = Profile.objects.create(
            user=user,
            nickname=user.username,
            birthdate=get_random_date(),
            gender=random.choice(choice_field["gender"]),
            preferred_gender=random.choice(choice_field["preferred_gender"]),
            mbti=random.choice(choice_field["mbti"]),
            height=random.randint(100, 300),
            religion=random.choice(choice_field["religion"]),
            smoking_status=bool(random.getrandbits(1)),
            drinking_status=random.choice(choice_field["drinking_status"]),
            location=random.choice(choice_field["location"]),
            bio=get_random_string(100),
        )

        profile.passion.set(
            random.sample(choice_field["passion"], settings.MAX_PASSION_NUM)
        )
