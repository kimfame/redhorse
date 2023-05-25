from django.db import models

from django.contrib.auth.models import User

from core.models import TimeStampedModel


class TemporaryPasswordIssueHistory(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Temporary Password Issue Histories"

    def __str__(self):
        return self.user.username
