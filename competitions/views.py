from django.shortcuts import render
from blog import models
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class viewCompetitions(generic.ListView, LoginRequiredMixin):
    model = models.Competition
    template_name = "Competitions/competitions.html"
    context_object_name = 'competitions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class addCompetition(generic.CreateView):
    model = models.Competition
    fields = ['title', 'location', 'description',
              'category', 'date', 'featuredImage']
    template_name = "Competitions/add_competition.html"
    success_url = reverse_lazy('competitions')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, 'Competiton created Succesfully')
        return super().form_valid(form)


class viewCompetitionDetailed(generic.DetailView):
    model = models.Competition
    template_name = 'Competitions/competition_detail.html'

