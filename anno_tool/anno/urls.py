#!/usr/bin/env python3
from django.urls import path

from . import views

app_name = 'anno'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:video_id>/', views.anno, name='anno'),
    path('start/', views.start, name='start'),
]
# vim: ts=4 sw=4 sts=4 expandtab
