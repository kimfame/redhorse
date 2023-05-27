import uuid

from django.contrib.auth.models import User
from django.db import models

from core.models import TimeStampedModel


class PhoneVerificationHistory(TimeStampedModel):
    phone_number = models.CharField(max_length=11)
    verification_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name_plural = "Phone Verification Histories"

    def __str__(self):
        return str(self.id)


class UserPhone(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11)

    def __str__(self):
        return self.phone_number
