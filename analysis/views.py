from django.http import HttpResponse
from django.shortcuts import render

from analysis.models import Notes


def index(self):
    note = Notes.objects.all()
    return HttpResponse(note[0].profile.user.username)
