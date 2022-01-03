from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from history.forms import AddNoteForm
from history.models import Note


@login_required
def add_note(request):
    if request.method == 'POST':
        new_note = AddNoteForm(request.POST)

        if new_note.is_valid():
            cd = new_note.cleaned_data
            cp = request.user.profile

            cp.change_earned(cd['earn'])
            total = cd['bank'] + cd['deposit'];
            daily_diff = cp.get_last_total()
            diff = total - cp.earned

            note = Note(profile=cp,
                        date=cd['date'],
                        earn=cd['earn'],
                        bank=cd['bank'],
                        deposit=cd['deposit'],
                        total=total,
                        daily_diff=daily_diff,
                        diff=diff,
                        comment=cd['comment'])
            note.save()

            cp.change_hold_and_diff()
    else:
        new_note = AddNoteForm()

    return render(request, 'add_note.html', {'form': new_note})


@login_required
def history(request):
    return render(request, 'history.html', {'profile': request.user.profile})


@login_required
def remove(request, part_id=None):
    note = Note.objects.filter(id=part_id)
    if note.count() > 0:
        request.user.profile.change_earned(-note[0].earn)
    note.delete()

    request.user.profile.change_hold_and_diff()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))