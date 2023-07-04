from django.shortcuts import render
from .models import Post, Comment
from django.views import generic


def index(request):
    return render(request, 'base.html')


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.order_by('timestamp')
    template_name = "index.html"
    context_object_name = 'posts'
