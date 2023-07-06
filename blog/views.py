from django.shortcuts import render
from .models import Post, Comment
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin



class index(generic.ListView, LoginRequiredMixin):
    model = Post
    queryset = Post.objects.order_by('timestamp')
    template_name = "index.html"
    context_object_name = 'posts'


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.order_by('timestamp')
    template_name = "index.html"
    context_object_name = 'posts'
