from django.shortcuts import render
from .models import Post, Comment
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class index(generic.ListView, LoginRequiredMixin):
    model = Post
    queryset = Post.objects.order_by('timestamp')
    template_name = "index.html"
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.order_by('timestamp')
    template_name = "index.html"
    context_object_name = 'posts'


class addPost(generic.CreateView):
    model = Post
    fields = ['title', 'content', 'image1', 'image2', 'category']
    template_name = "Posts/add_post.html"
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        messages.success(self.request, 'Post added Succesfully')
        return super().form_valid(form)


class editPost(generic.UpdateView):
    model = Post
    fields = ['title', 'content', 'image1', 'image2', 'category']
    template_name = 'Posts/edit_post.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        messages.success(self.request, 'Post updated Succesfully')
        return super().form_valid(form)


class deletePost(generic.DeleteView):
    model = Post
    template_name = 'Posts/delete_post.html'
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post Deleted Successfully')
        return super().delete(request, *args, **kwargs)


class viewPost(generic.DetailView):
    model = Post
    template_name = 'Posts/post_detail.html'

    def get_object(self):
        obj = super().get_object()
        print(obj.user_id)  # or use logging
        return obj
