from django.http import HttpResponse
from django.shortcuts import render

from account.models import Profile


def index(self):
    p = Profile.objects.all()
    return HttpResponse(p[0].notes_set.all()[0].comment)
