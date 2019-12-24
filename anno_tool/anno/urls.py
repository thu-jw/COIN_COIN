#!/usr/bin/env python3
from django.urls import path

from . import views

app_name = 'anno'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:video_id>/<int:start_step>', views.anno, name='anno'),
    path('<int:video_id>/navigate', views.navigate, name='navigate'),
    path('<int:video_id>/edit', views.edit, name='edit'),
    path('start/', views.start, name='start'),
    path('resume/', views.resume, name='resume'),
    path('help/', views.help, name='help'),
]
# vim: ts=4 sw=4 sts=4 expandtab
