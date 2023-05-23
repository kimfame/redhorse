import logging
import random

from django.contrib.auth.models import User
from django.db import OperationalError

from chat_message.factories import ChatMessageFactory
from chat_room.factories import ChatRoomFactory
from match.factories import MatchFactory
from profile_picture.factories import ProfilePictureFactory
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


def create_test_users():
    logger.info("Create fake users")
    profile_list = ProfileFactory.create_batch(10)

    for profile in profile_list:
        ProfilePictureFactory.create(main=True, user=profile.user)
        ProfilePictureFactory.create_batch(size=2, user=profile.user)

    user_list = [profile.user for profile in profile_list]
    create_matches(user_list)


def create_pair_messages(room, pair_size=None):
    pair_size = pair_size if pair_size else random.randint(2, 5)
    users = room.users.all()

    for _ in range(pair_size):
        for user in users:
            ChatMessageFactory(room=room, user=user)


def create_matches(user_list):
    def create_mutual_likes(user_1, user_2):
        MatchFactory(
            sender=user_1,
            receiver=user_2,
            is_liked=True,
            is_matched=True,
        )
        MatchFactory(
            sender=user_2,
            receiver=user_1,
            is_liked=True,
            is_matched=True,
        )

        room = ChatRoomFactory(users=[user_1, user_2])
        create_pair_messages(room, 100)

    for i in range(2):
        j = i + 1 if i == 0 else i + 3
        create_mutual_likes(user_list[i], user_list[j])

        MatchFactory(
            sender=user_list[i],
            receiver=user_list[j + 1],
            is_liked=True,
            is_matched=False,
        )
        MatchFactory(
            sender=user_list[j + 1],
            receiver=user_list[i],
            is_liked=False,
            is_matched=False,
        )

        MatchFactory(
            sender=user_list[i],
            receiver=user_list[j + 2],
            is_liked=False,
            is_matched=False,
        )
        MatchFactory(
            sender=user_list[j + 2],
            receiver=user_list[i],
            is_liked=True,
            is_matched=False,
        )

        MatchFactory(
            sender=user_list[i],
            receiver=user_list[j + 3],
            is_liked=False,
            is_matched=False,
        )
        MatchFactory(
            sender=user_list[j + 3],
            receiver=user_list[i],
            is_liked=False,
            is_matched=False,
        )

        create_mutual_likes(user_list[i], user_list[j + 4])
        create_mutual_likes(user_list[i], user_list[j + 5])
