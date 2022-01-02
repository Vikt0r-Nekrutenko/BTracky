from django.urls import path
from . import views

app_name = 'history'

urlpatterns = [
    path('', views.index, name='index'),
    path(r'<part_id>', views.remove, name=''),
]
