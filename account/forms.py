from django import forms
from django.contrib.auth.models import User


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
