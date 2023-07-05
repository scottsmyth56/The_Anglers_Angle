from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import  RegistrationForm


def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'Auth/register_user.html', {'form': form})

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return render(request, 'Auth/register_user.html', {'form': form})
        else:
            return render(request, 'Auth/register_user.html', {'form': form})
