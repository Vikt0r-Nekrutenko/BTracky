from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from history.forms import AddNoteForm
from history.models import Note


@login_required
def index(request):
    if request.method == 'POST':
        new_note = AddNoteForm(request.POST)

        if new_note.is_valid():
            request.user.profile.change_earned(new_note.cleaned_data['earn'])

            total = new_note.cleaned_data['bank']+new_note.cleaned_data['deposit'];
            daily_diff = 0

            if request.user.profile.notes_set.count() > 0:
                daily_diff = total - request.user.profile.notes_set.last().total
            diff = total - request.user.profile.earned

            note = Note(profile=request.user.profile,
                        date=new_note.cleaned_data['date'],
                        earn=new_note.cleaned_data['earn'],
                        bank=new_note.cleaned_data['bank'],
                        deposit=new_note.cleaned_data['deposit'],
                        total=total,
                        daily_diff=daily_diff,
                        diff=diff,
                        comment=new_note.cleaned_data['comment'])
            note.save()

            request.user.profile.change_hold_and_diff()

        return render(request, 'dashboard.html', {'user': request.user})
    else:
        new_note = AddNoteForm()

    return render(request, 'index.html', {'form': new_note,
                                          'profile': request.user.profile})


@login_required
def remove(request, part_id=None):
    note = Note.objects.filter(id=part_id)
    if note.count() > 0:
        request.user.profile.change_earned(-note[0].earn)
    note.delete()

    request.user.profile.change_hold_and_diff()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))