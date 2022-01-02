from django.contrib import admin
from django.contrib.admin import ModelAdmin

from history.models import Note


@admin.register(Note)
class NotesAdmin(ModelAdmin):
    list_display = ['profile', 'date', 'earn', 'bank', 'deposit', 'comment']
