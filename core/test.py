from datetime import date

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from user.factories import UserFactory


def get_client_with_login_status(user: User = None):
    client = APIClient()
    user = user if user else UserFactory()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


def get_random_adult_birthdate() -> tuple[date, date]:
    today = date.today()
    end_date = date(year=(today.year - 20), month=today.month, day=today.day)
    start_date = date(year=(today.year - 100), month=today.month, day=today.day)

    return start_date, end_date
