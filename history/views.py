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
            request.user.profile.earned += new_note.cleaned_data['earn']
            request.user.profile.save()

            total = new_note.cleaned_data['bank']+new_note.cleaned_data['deposit'];
            daily_diff = 0

            if request.user.profile.notes_set.count() > 0:
                daily_diff = total - request.user.profile.notes_set.last().total
            diff = total - request.user.profile.earned

            note = Notes(profile=request.user.profile,
                         date=new_note.cleaned_data['date'],
                         earn=new_note.cleaned_data['earn'],
                         bank=new_note.cleaned_data['bank'],
                         deposit=new_note.cleaned_data['deposit'],
                         total=total,
                         daily_diff=daily_diff,
                         diff=diff,
                         comment=new_note.cleaned_data['comment'])
            note.save()

            request.user.profile.hold = request.user.profile.notes_set.last().total
            request.user.profile.difference = request.user.profile.notes_set.last().diff
            request.user.profile.save()

        return render(request, 'dashboard.html', {'user': request.user})
    else:
        new_note = AddNoteForm()

    return render(request, 'index.html', {'form': new_note,
                                          'profile': request.user.profile})


@login_required
def remove(request, part_id=None):
    note = Notes.objects.filter(id=part_id)
    note.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))