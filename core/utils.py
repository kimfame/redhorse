from __future__ import annotations

import random
import re
import string
import sys

from datetime import date, datetime, timedelta
from io import BytesIO
from secrets import choice

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import ImageField
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from PIL import Image

from match.models import Match
from option_code.models import OptionCode
from user.factories import UserFactory
from user_profile.models import Profile


def calculate_age(birthdate: date) -> int:
    today = date.today()
    return (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    )


def compress_image(image: ImageField):
    pil_image = Image.open(image)
    pil_image = pil_image.convert("RGB")

    stream_image = BytesIO()
    pil_image.save(stream_image, format="JPEG", quality=70)
    stream_image.seek(0)

    new_image = InMemoryUploadedFile(
        file=stream_image,
        field_name="ImageField",
        name=image.name,
        content_type="image/jpeg",
        size=sys.getsizeof(stream_image),
        charset=None,
    )
    return new_image


def get_client_with_login_status(client: APIClient = APIClient(), user: User = None):
    user = user if user else UserFactory()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


def get_current_and_past_time(minutes: int) -> tuple[datetime, datetime]:
    end_datetime = datetime.now()
    start_datetime = end_datetime - timedelta(minutes=minutes)

    return (start_datetime, end_datetime)


def get_option_code_list(group_name: str) -> list[str]:
    return list(
        OptionCode.objects.filter(group__name=group_name).values_list(
            "value",
            flat=True,
        )
    )


def get_random_adult_birthdate() -> tuple[date, date]:
    today = date.today()
    end_date = date(year=(today.year - 20), month=today.month, day=today.day)
    start_date = date(year=(today.year - 100), month=today.month, day=today.day)

    return start_date, end_date


def get_random_string(len: int) -> str:
    return "".join([choice(string.ascii_letters + string.digits) for _ in range(len)])


def get_random_verification_code() -> str:
    return f"{random.randint(100000, 999999)}"


def get_remaining_like_num(user_id: int) -> int:
    today_match = Match.objects.filter(
        sender=user_id,
        created_datetime__date=date.today(),
    ).count()

    return settings.MAX_LIKE_NUM - today_match


def get_user_object(request: Request) -> User:
    if isinstance(request.user, User):
        return request.user
    else:
        return get_object_or_404(User, id=request.user.id)


def get_user_object_with_profile(request: Request) -> User:
    if isinstance(request.user, User):
        user = request.user
    else:
        user = get_object_or_404(
            User.objects.select_related("profile"), id=request.user.id
        )

    try:
        user.profile
        return user
    except Profile.DoesNotExist:
        raise Http404


def is_adult(birthdate: date) -> bool:
    age = calculate_age(birthdate)

    if age > 18:
        return True
    else:
        return False


def is_valid_phone_number(phone_number: str) -> bool:
    regex = re.compile(r"^010\d{8}$")

    if regex.search(phone_number):
        return True
    else:
        return False


def is_valid_username(username: str) -> bool:
    regex = re.compile(r"^[\w-]{5,20}$")

    if regex.search(username):
        return True
    else:
        return False
