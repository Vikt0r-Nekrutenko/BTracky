from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from history.forms import AddNoteForm
from history.models import Notes


@login_required
def index(request):
    if request.method == 'POST':
        new_note = AddNoteForm(request.POST)

        if new_note.is_valid():
            note = Notes(profile=request.user.profile,
                         date=new_note.cleaned_data['date'],
                         earn=new_note.cleaned_data['earn'],
                         bank=new_note.cleaned_data['bank'],
                         deposit=new_note.cleaned_data['deposit'],
                         comment=new_note.cleaned_data['comment'])

            note.save()

    else:
        new_note = AddNoteForm()

    return render(request, 'index.html', {'form': new_note,
                                          'profile': request.user.profile})


@login_required
def remove(request, part_id=None):
    obj = Notes.objects.filter(id=part_id)
    obj.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))