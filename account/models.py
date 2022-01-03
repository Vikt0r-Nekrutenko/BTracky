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
        if self.note_set.count() > 0:
            self.hold = self.note_set.first().total
            self.difference = self.hold - self.earned
        else:
            self.hold = 0
            self.difference = 0
        self.save()

    def get_last_total(self):
        if self.note_set.count() > 0:
            return self.note_set.first().total
        return 0