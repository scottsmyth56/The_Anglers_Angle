from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from blog.models import Group, UserGroup, Post, User
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class viewGroups(LoginRequiredMixin, generic.ListView):
    model = Group
    template_name = "Groups/groups.html"
    context_object_name = 'groups'

    def get_queryset(self):
        return Group.objects.filter(is_approved=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class addGroup(LoginRequiredMixin, generic.CreateView):
    model = Group
    fields = ['group_name', 'description', 'featuredImage']
    template_name = "Groups/add_group.html"
    success_url = reverse_lazy('groups')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.is_approved = False
        messages.success(
            self.request, f'Group "{form.instance.group_name}" created successfully, waiting for admin approval')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'Form validation failed: {}'.format(form.errors))
        return super().form_invalid(form)


class viewGroup(LoginRequiredMixin, generic.DetailView):
    model = Group
    template_name = 'Groups/groupIndex.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_user'] = UserGroup.objects.filter(
            group_id=self.object, user_id=self.request.user)

        context['group_member'] = User.objects.filter(
            usergroup__group_id=self.object)

        context['posts'] = Post.objects.filter(group=self.object)

        return context


class enterGroup(LoginRequiredMixin, generic.CreateView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        group = get_object_or_404(Group, pk=pk)
        if UserGroup.objects.filter(user_id=request.user, group_id=group).exists():
            UserGroup.objects.filter(
                user_id=request.user, group_id=group).delete()
            messages.success(
                request, f'You have left "{group.group_name}" ')
        else:
            UserGroup.objects.create(
                user_id=request.user, group_id=group)
            messages.success(
                request, f'You have joined "{group.group_name}" Welcome!')

        return redirect('viewGroup', pk=pk)


class editGroup(LoginRequiredMixin, generic.UpdateView):
    model = Group
    fields = ['group_name', 'description', 'featuredImage']
    template_name = 'Groups/edit_group.html'
    success_url = reverse_lazy('groups')

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        messages.success(self.request, 'Group Details updated Succesfully')
        return super().form_valid(form)


class deleteGroup(LoginRequiredMixin, generic.DeleteView):
    model = Group
    template_name = 'Groups/delete_group.html'
    success_url = reverse_lazy('groups')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Group Deleted Successfully')
        return super().delete(request, *args, **kwargs)


class addGroupPost(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'content', 'image1', 'image2', 'category']
    template_name = "Posts/add_post.html"
    success_url = reverse_lazy('viewGroup')

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        group_id = self.kwargs['pk']
        group = get_object_or_404(Group, pk=group_id)
        form.instance.group = group
        messages.success(self.request, 'Group Post added Succesfully')
        form.save()
        return redirect('viewGroup', pk=group_id)
    #  return super().form_valid(form)


class editGroupPost(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'content', 'image1', 'image2', 'category']
    template_name = 'Posts/edit_post.html'
    # success_url = reverse_lazy('vi')

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs.get('pk'))

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        messages.success(self.request, 'Group Post updated Successfully')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('viewGroup', kwargs={'pk': self.object.group.pk})


class deleteGroupPost(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'Posts/delete_post.html'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post Deleted Successfully')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        group_id = self.object.group.pk
        return reverse('viewGroup', kwargs={'pk': group_id})
