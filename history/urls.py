from django.urls import path
from . import views

app_name = 'history'

urlpatterns = [
    path('add_note', views.add_note, name='add_note'),
    path('', views.history, name='history'),
    path(r'<part_id>', views.remove, name='remove'),
]
