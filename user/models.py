from django.db import models

from django.contrib.auth.models import User


class TemporaryPasswordIssueHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Temporary Password Issue Histories"

    def __str__(self):
        return self.user.username
