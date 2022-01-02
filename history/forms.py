from django import forms
from django.forms import ModelForm

from account.models import Profile
from history.models import Note


class AddNoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['date', 'earn', 'bank', 'deposit', 'comment']

    def __init__(self, *args, **kwargs):
        super(AddNoteForm, self).__init__(*args, **kwargs)
        self.fields['date'] = forms.DateField(widget=forms.SelectDateWidget)