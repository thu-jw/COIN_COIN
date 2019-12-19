#!/usr/bin/env python3
from django.shortcuts import render
from django.http import HttpResponseRedirect

def index(request):
    return HttpResponseRedirect('anno')
# vim: ts=4 sw=4 sts=4 expandtab
