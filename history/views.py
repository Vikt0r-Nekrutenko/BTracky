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
            request.user.profile.change_earned(new_note.cleaned_data['earn'])

            total = new_note.cleaned_data['bank'] + new_note.cleaned_data['deposit'];
            daily_diff = request.user.profile.get_last_total()
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