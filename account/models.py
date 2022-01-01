from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    earned = models.PositiveIntegerField(default=0)
    hold = models.IntegerField(default=0)
    difference = models.IntegerField(default=0)