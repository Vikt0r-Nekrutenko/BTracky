from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render

from account.models import Profile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    repeat_password = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']

    def clean_repeat_password(self):
        cd = self.cleaned_data

        if cd['password'] != cd['repeat_password']:
            raise forms.ValidationError('Passwords don\'t match!')

        return cd['repeat_password']


@login_required
def dashboard(request):
    lm = datetime.today() - timedelta(days=30)
    lmi = request.user.profile.note_set.filter(date__gte=lm)
    daily_pnl = request.user.profile.note_set.first().daily_diff / request.user.profile.earned * 100
    mpnl = (lmi.first().diff - lmi.last().diff) / request.user.profile.earned * 100

    return render(request, 'dashboard.html', {'user': request.user,
                                              'daily_pnl': daily_pnl,
                                              'lmi': mpnl,
                                              })


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