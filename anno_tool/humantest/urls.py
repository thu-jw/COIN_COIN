#!/usr/bin/env python3
from django.urls import path

from . import views

app_name = 'humantest'

urlpatterns = [
    path('', views.start, name='index'),
    path('<str:setting>/<str:phase>/start', views.start, name='start'),
    path('stat/', views.stat, name='stat'),
    path('start/', views.start, name='start'),
    path('<int:qa_id>', views.qa, name='qa'),
    path('<int:qa_id>/choose', views.choose, name='choose'),
]
# vim: ts=4 sw=4 sts=4 expandtab
