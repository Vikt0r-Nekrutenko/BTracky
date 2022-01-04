from django.contrib.auth.decorators import login_required
from django.forms import forms
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
            total = cd['bank'] + cd['deposit']
            daily_diff = total - cp.get_last_total()
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
            raise forms.ValidationError('Note isn\'t valid!')
    else:
        new_note = AddNoteForm()

    return render(request, 'add_note.html', {'form': new_note,
                                             'last_note': Note.last_day_info(request.user.id)})


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

'''
cp = request.user.profile
    wb = load_workbook(filename='Finance\'s.xlsx')
    sheet = wb['finances']

    n = 1
    for n in range(188, 189):
        date1 = sheet.cell(n, 1).value
        date2 = timezone.now()

        date1 = datetime.datetime(date1.year,
                                  date1.month,
                                  date1.day,
                                  date2.hour,
                                  date2.minute,
                                  date2.second,
                                  date2.microsecond)

        #cp.change_earned(sheet.cell(n, 2).value)
        #total = sheet.cell(n, 3).value + sheet.cell(n, 4).value
        #daily_diff = total - cp.get_last_total()
        #diff = total - cp.earned

        note = Note(profile=request.user.profile,
                        date=date1,
                        earn=sheet.cell(n, 2).value,
                        bank=sheet.cell(n, 3).value,
                        deposit=sheet.cell(n, 4).value,
                        total=total,
                        daily_diff=daily_diff,
                        diff=diff,
                        comment=sheet.cell(n, 8).value)
        #note.save()
        #cp.change_hold_and_diff()
'''