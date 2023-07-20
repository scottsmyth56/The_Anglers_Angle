from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout
from .forms import RegistrationForm, LoginForm, EditUserForm, ResetPasswordForm
from blog.models import User,Post
from django.contrib.auth.decorators import login_required
import os


def register(request):
   if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        return redirect('login')
    else:
        for field in form.errors:
            message = form.errors[field][0] 
            messages.error(request, message)
        return render(request, 'Auth/register_user.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = LoginForm()
 
    return render(request, 'Auth/login_user.html', {'form': form})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = EditUserForm(instance=request.user)
    return render(request, 'Auth/edit_profile.html', {'form': form})


@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(user_id=user)  
    context = {
        'user': user,
        'posts': user_posts,
    }
    return render(request, 'Auth/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password successfully changed.')
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, 'Please confirm new passwords match and your current password is correct and try again')
    else:
        form = ResetPasswordForm(request.user)
    return render(request, 'Auth/change_password.html', {'form': form})
