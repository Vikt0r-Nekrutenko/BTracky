import datetime

from django.utils import timezone
from django.db import models

from account.models import Profile


class Notes(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(default="2020-1-1")
    earn = models.PositiveIntegerField(default=0)
    bank = models.IntegerField(default=0)
    deposit = models.PositiveIntegerField(default=0)
    total = models.IntegerField(default=0)
    daily_diff = models.IntegerField(default=0)
    diff = models.IntegerField(default=0)
    comment = models.CharField(max_length=255)

    class Meta:
        ordering = ['-date']
