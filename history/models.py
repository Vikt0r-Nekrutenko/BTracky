import datetime

from django.utils import timezone
from django.db import models

from account.models import Profile


class Note(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    earn = models.PositiveIntegerField(default=0)
    bank = models.IntegerField(default=0)
    deposit = models.PositiveIntegerField(default=0)
    total = models.IntegerField(default=0)
    daily_diff = models.IntegerField(default=0)
    diff = models.IntegerField(default=0)
    comment = models.CharField(default='nothing', max_length=255)

    class Meta:
        ordering = ['-date']
