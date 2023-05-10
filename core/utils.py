import re
import string
import sys

from datetime import date, datetime, timedelta
from io import BytesIO
from secrets import choice
from typing import Tuple

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import ImageField
from PIL import Image

from common_code.models import CommonCode


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


def calculate_age(birthdate: date) -> int:
    today = date.today()
    return (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    )


def is_adult(birthdate: date) -> bool:
    age = calculate_age(birthdate)

    if age > 18:
        return True
    else:
        return False


def get_current_and_past_time(minutes: int) -> Tuple[datetime, datetime]:
    end_datetime = datetime.now()
    start_datetime = end_datetime - timedelta(minutes=minutes)

    return (start_datetime, end_datetime)


def get_random_string(len: int) -> str:
    return "".join([choice(string.ascii_letters + string.digits) for _ in range(len)])


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


def get_common_code_list(group_name: str) -> list:
    return list(
        CommonCode.objects.filter(group__name=group_name).values_list(
            "value",
            flat=True,
        )
    )
