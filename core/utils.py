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
from django.db import connection
from django.db.models import ImageField
from PIL import Image

from option_code.models import OptionCode
from match.models import Match


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


def fetchall_from_db(query: str, query_params: dict[str, str]) -> list[dict[str, any]]:
    with connection.cursor() as cursor:
        cursor.execute(query, query_params)
        description = cursor.description
        rows = cursor.fetchall()

    columns = [col[0] for col in description]
    return [dict(zip(columns, row)) for row in rows]


def get_option_code_list(group_name: str) -> list[str]:
    return list(
        OptionCode.objects.filter(group__name=group_name).values_list(
            "value",
            flat=True,
        )
    )


def get_current_and_past_time(minutes: int) -> tuple[datetime, datetime]:
    end_datetime = datetime.now()
    start_datetime = end_datetime - timedelta(minutes=minutes)

    return (start_datetime, end_datetime)


def get_random_string(len: int) -> str:
    return "".join([choice(string.ascii_letters + string.digits) for _ in range(len)])


def get_random_verification_code() -> str:
    return f"{random.randint(100000, 999999)}"


def get_remaining_like_num(user: User) -> int:
    today_match = Match.objects.filter(
        sender=user,
        created_at__date=date.today(),
    ).count()

    return settings.MAX_LIKE_NUM - today_match


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
