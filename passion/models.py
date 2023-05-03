from django.db import models


class Passion(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name
