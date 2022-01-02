from django.contrib import admin
from django.contrib.admin import ModelAdmin

from analysis.models import Notes


@admin.register(Notes)
class NotesAdmin(ModelAdmin):
    list_display = ['profile', 'date', 'earn', 'bank', 'deposit', 'comment']
