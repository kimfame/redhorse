import logging

from django.contrib.auth.models import User
from django.db import OperationalError

from user_profile.factories import ProfileFactory

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


def create_test_users(user_num=10):
    logger.info("Create fake users")
    ProfileFactory.create_batch(user_num)
