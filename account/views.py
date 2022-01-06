from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from account.models import Profile
from .forms import UserRegistrationForm


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'registration/registration_done.html', {'username': new_user.username})

    else:
        user_form = UserRegistrationForm()

    return render(request, 'registration/registration.html', {'user_form': user_form})