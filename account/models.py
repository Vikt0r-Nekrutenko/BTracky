from django.conf import settings
from django.db import models
from datetime import datetime, timedelta

from django.db.models import Q
from django.forms import forms


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

    def get_last_bank(self):
        if self.note_set.count() > 0:
            return self.note_set.first().bank

    def get_pnl_by_period(self, period=1):
        p = datetime.today() - timedelta(days=period)
        notes_by_p = self.note_set.filter(~Q(date__gte=p))

        if notes_by_p.count() == 1:
            return notes_by_p.first().daily_diff

        elif notes_by_p.count() > 0:
            return self.note_set.first().total - notes_by_p.first().total
        return 0

    def get_percentage_pnl_by_period(self, period=1):
        pnl = self.get_pnl_by_period(period)

        if pnl != 0:
            return pnl / self.earned * 100
        return 0

    def get_today_pnl(self):
        return self.get_pnl_by_period()

    def get_week_pnl(self):
        return self.get_pnl_by_period(7)

    def get_month_pnl(self):
        return self.get_pnl_by_period(30)

    def get_three_month_pnl(self):
        return self.get_pnl_by_period(90)

    def get_half_year_pnl(self):
        return self.get_pnl_by_period(180)

    def get_p_today_pnl(self):
        return self.get_percentage_pnl_by_period()

    def get_p_week_pnl(self):
        return self.get_percentage_pnl_by_period(7)

    def get_p_month_pnl(self):
        return self.get_percentage_pnl_by_period(30)

    def get_p_three_month_pnl(self):
        return self.get_percentage_pnl_by_period(90)

    def get_p_half_year_pnl(self):
        return self.get_percentage_pnl_by_period(180)
