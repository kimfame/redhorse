import uuid

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel
from user_profile import choices

from user_profile.validators import PassionsValidator, PASSIONS_JSON_FIELD_SCHEMA


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nickname = models.CharField(max_length=20, unique=True)
    birthdate = models.DateField()
    gender = models.CharField(max_length=1, choices=choices.Gender.choices)
    preferred_gender = models.CharField(
        max_length=1, choices=choices.PreferredGender.choices
    )
    mbti = models.CharField(
        max_length=4,
        validators=[RegexValidator(regex="^[EI]{1}[NS]{1}[FT]{1}[JP]{1}$")],
    )
    passions = models.JSONField(
        max_length=100,
        null=True,
        blank=True,
        validators=[PassionsValidator(limit_value=PASSIONS_JSON_FIELD_SCHEMA)],
    )
    height = models.CharField(max_length=3)
    religion = models.CharField(max_length=3, choices=choices.Religion.choices)
    smoking_status = models.BooleanField()
    drinking_status = models.CharField(
        max_length=2, choices=choices.DrinkingStatus.choices
    )
    location = models.CharField(max_length=2, choices=choices.Location.choices)
    bio = models.CharField(max_length=500)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
