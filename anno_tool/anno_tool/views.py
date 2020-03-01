#!/usr/bin/env python3
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def index(request):
    return redirect('humantest/')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/humantest/start')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
# vim: ts=4 sw=4 sts=4 expandtab
