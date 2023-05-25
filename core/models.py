from django.db import models


class TimeStampedModel(models.Model):
    updated_datetime = models.DateTimeField(auto_now=True)
    created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
