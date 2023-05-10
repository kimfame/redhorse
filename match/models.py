from django.db import models
from django.contrib.auth.models import User


class Match(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name="receiver", on_delete=models.SET_NULL, null=True
    )
    is_liked = models.BooleanField(default=False)
    is_matched = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Matches"

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
