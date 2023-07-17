from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout
from .forms import RegistrationForm, LoginForm, EditUserForm


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
            print("sending to login")
            return redirect('login')
        else:
            return render(request, 'Auth/register_user.html', {'form': form})


def login(request):
    if request.method == 'POST':
        print(request.POST)
        form = LoginForm(request.POST)
        print(f"form is valid: {form.is_valid()}")
        if form.errors:
            print(f"errors: {form.errors}")
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"{username} / {password}")
            user = authenticate(username=username, password=password)
            if user is not None:
                print("user authenticated")
                auth_login(request, user)
                return redirect('post-list')
            else:
                print("user not authenticated")
    else:
        form = LoginForm()

    return render(request, 'Auth/login_user.html', {'form': form})


def edit_profile(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = EditUserForm(instance=request.user)
    return render(request, 'Auth/edit_profile.html', {'form': form})
