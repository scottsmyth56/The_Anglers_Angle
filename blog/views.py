from django.shortcuts import render
from .models import Post, Comment


def index(request):
    return render(request, 'base.html')
