import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from passion.models import Passion


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nickname = models.CharField(max_length=20, unique=True)
    birthdate = models.DateField()
    gender = models.CharField(max_length=1)
    preferred_gender = models.CharField(max_length=1)
    mbti = models.CharField(max_length=4)
    passion = models.ManyToManyField(Passion, blank=True)
    height = models.CharField(max_length=3)
    religion = models.CharField(max_length=3)
    smoking_status = models.BooleanField(default=False)
    drinking_status = models.CharField(max_length=2)
    location = models.CharField(max_length=2)
    bio = models.CharField(max_length=500)
    is_banned = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_passion_list(self):
        return [passion.name for passion in self.passion.all()]
