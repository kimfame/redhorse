from django.db import models
from django.contrib.auth.models import User

from core.models import TimeStampedModel


class Match(TimeStampedModel):
    sender = models.ForeignKey(
        User, related_name="sender", on_delete=models.SET_NULL, null=True
    )
    receiver = models.ForeignKey(
        User, related_name="receiver", on_delete=models.SET_NULL, null=True
    )
    is_liked = models.BooleanField(default=False)
    is_matched = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Matches"
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "receiver"], name="unique_sender_receiver_combination"
            )
        ]

    def __str__(self):
        return str(self.id)
