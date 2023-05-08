import uuid

from django.db import models

from core.utils import compress_image
from basic_profile.models import Profile


def get_profile_picture_path(instance, filename):
    return f"profile_picture/{instance.profile.uuid}/{uuid.uuid4()}.jpg"


class ProfilePicture(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    main = models.BooleanField(default=False)
    image = models.ImageField(upload_to=get_profile_picture_path)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.uuid)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.image = compress_image(self.image)
        return super(ProfilePicture, self).save(*args, **kwargs)
