from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from analysis.models import Notes


@login_required
def index(request):
    return render(request, 'index.html', {'profile': request.user.profile})