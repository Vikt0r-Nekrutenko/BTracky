from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    earned = models.PositiveIntegerField(default=0)
    hold = models.IntegerField(default=0)
    difference = models.IntegerField(default=0)

    def change_earned(self, value):
        self.earned += value
        self.save()

    def change_hold_and_diff(self):
        if self.notes_set.count() > 0:
            self.hold = self.notes_set.last().total
            self.difference = self.notes_set.last().diff
        else:
            self.hold = 0
            self.difference = 0
        self.save()