import re
import string

from datetime import date, datetime, timedelta
from secrets import choice
from typing import Tuple


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


def is_adult(birthdate: date) -> bool:
    today = date.today()
    age = (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    )

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
