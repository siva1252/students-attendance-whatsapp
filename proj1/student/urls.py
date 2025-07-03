from django.urls import path
from . import views

urlpatterns = [
    path('attendance/', views.mark_attendance, name='attendance'),
]
