from django.db import models


class CommonCodeGroup(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class CommonCode(models.Model):
    group = models.ForeignKey(CommonCodeGroup, on_delete=models.CASCADE)
    sub_id = models.PositiveSmallIntegerField(default=0)
    value = models.CharField(max_length=20)

    def __str__(self):
        return self.value
