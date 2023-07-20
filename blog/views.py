
from django.shortcuts import render, get_object_or_404, redirect
from models import Post, Comment, Like
from django.views import generic, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class index(LoginRequiredMixin, generic.ListView):

    """This class represents the index page. It requires the user to be logged in."""

    model = Post
    queryset = Post.objects.order_by('timestamp')
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['posts'] = Post.objects.filter(group=None)
        return context


class PostList(LoginRequiredMixin, generic.ListView):

    """This class represents the list of all posts, visible only to logged-in users."""

    model = Post
    queryset = Post.objects.order_by('timestamp')
    template_name = 'index.html'
    context_object_name = 'posts'


class addPost(LoginRequiredMixin, generic.CreateView):

    '''This class provides the add post functionality for logged-in users.'''

    model = Post
    fields = ['title', 'content', 'image1', 'image2', 'category']
    template_name = 'Posts/add_post.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        messages.success(self.request, 'Post added Succesfully')
        return super().form_valid(form)


class editPost(LoginRequiredMixin, generic.UpdateView):

    '''This class provides the edit post functionality for logged-in users.'''

    model = Post
    fields = ['title', 'content', 'image1', 'image2', 'category']
    template_name = 'Posts/edit_post.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        messages.success(self.request, 'Post updated Succesfully')
        return super().form_valid(form)


class deletePost(LoginRequiredMixin, generic.DeleteView):

    '''This class provides the delet post functionality for logged-in users.'''

    model = Post
    template_name = 'Posts/delete_post.html'
    success_url = reverse_lazy('index')

    def delete(
        self,
        request,
        *args,
        **kwargs
    ):
        messages.success(request, 'Post Deleted Successfully')
        return super().delete(request, *args, **kwargs)


class viewPost(LoginRequiredMixin, generic.DetailView):

    '''This class provides the view post functionality for logged-in users.'''

    model = Post
    template_name = 'Posts/post_detail.html'

    def get_object(self):
        obj = super().get_object()
        print (obj.user_id)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context['comments'] = Comment.objects.filter(post_id=post)
        context['likes'] = Like.objects.filter(post_id=post).count()
        context['user_has_liked'] = Like.objects.filter(
            post_id=post, user_id=self.request.user).exists()
        return context


class likePost(LoginRequiredMixin, View):

    '''This class provides the like post functionality for logged-in users.'''

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        Like.objects.create(user_id=request.user, post_id=post)
        return redirect('viewPost', pk=post.pk)


class unlikePost(LoginRequiredMixin, View):

    '''This class provides the unlike post functionality for logged-in users.'''

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        Like.objects.filter(user_id=request.user, post_id=post).delete()
        return redirect('viewPost', pk=post.pk)


class addComment(LoginRequiredMixin, View):

    '''This class provides the add comment on a post functionality for logged-in users.'''

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        Comment.objects.create(user_id=request.user, post_id=post,
                               comment=request.POST['comment'])
        return redirect('viewPost', pk=post.pk)


class editComment(LoginRequiredMixin, generic.UpdateView):

    '''This class provides the edit comment on a post functionality for logged-in users.'''

    model = Comment
    fields = ['comment']
    template_name = 'Posts/edit_comment.html'

    def get_success_url(self):
        messages.success(self.request, 'Comment updated Succesfully')
        return reverse_lazy('viewPost',
                            kwargs={'pk': self.object.post_id.pk})


class deleteComment(LoginRequiredMixin, generic.DeleteView):

    '''This class provides the delete comment on a post functionality for logged-in users.'''

    model = Comment
    template_name = 'Posts/delete_comment.html'

    def get_success_url(self):
        messages.success(self.request, 'Comment Deleted Succesfully')
        return reverse_lazy('viewPost',
                            kwargs={'pk': self.object.post_id.pk})
