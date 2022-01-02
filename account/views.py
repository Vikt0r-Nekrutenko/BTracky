from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from account.models import Profile


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'profile': Profile.objects.all()[0]})
