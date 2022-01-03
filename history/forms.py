from django import forms
from django.forms import ModelForm

from account.models import Profile
from history.models import Note
from django.utils import timezone


class AddNoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['date', 'earn', 'bank', 'deposit', 'comment']

    def __init__(self, *args, **kwargs):
        super(AddNoteForm, self).__init__(*args, **kwargs)
        years = tuple(n for n in range(timezone.now().year-10, timezone.now().year + 1))
        self.fields['date'] = forms.DateTimeField(initial=timezone.now)
        self.fields['earn'] = forms.IntegerField(initial=0, min_value=0)
        self.fields['deposit'] = forms.IntegerField(initial=0, min_value=0)