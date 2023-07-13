from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from blog.models import Group, UserGroup,Post,User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class viewGroups(generic.ListView, LoginRequiredMixin):
    model = Group
    template_name = "Groups/groups.html"
    context_object_name = 'groups'

    def get_queryset(self):
        return Group.objects.filter(is_approved=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class addGroup(generic.CreateView):
    model = Group
    fields = ['group_name', 'description','featuredImage']
    template_name = "Groups/add_group.html"
    success_url = reverse_lazy('groups')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.is_approved = False
        messages.success(self.request, 'Your Group creation is pending admin approval')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Form validation failed: {}'.format(form.errors))
        return super().form_invalid(form)


class viewGroup(generic.DetailView):
    model = Group
    template_name = 'Groups/groupIndex.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_user'] = UserGroup.objects.filter(
            group_id=self.object, user_id=self.request.user)

        context['group_member'] = User.objects.filter(
            usergroup__group_id=self.object)

        context['posts'] = Post.objects.filter(group = self.object )

        return context

