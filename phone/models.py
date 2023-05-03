import uuid

from django.contrib.auth.models import User
from django.db import models


class PhoneVerificationHistory(models.Model):
    phone_number = models.CharField(max_length=11)
    verification_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Phone Verification Histories"

    def __str__(self):
        return self.verification_code


class UserPhone(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number
