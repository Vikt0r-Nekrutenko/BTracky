from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'history'

urlpatterns = [
    path('add_note', views.add_note, name='add_note'),
    path('', views.history, name='history'),
    path(r'<part_id>', views.remove, name='remove'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
