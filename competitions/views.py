from django.shortcuts import render, get_object_or_404, redirect
from blog import models
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['competition_user'] = models.CompetitionUser.objects.filter(
            competition_id=self.object, user_id=self.request.user)
        return context


class enterCompetition(generic.CreateView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        competition = get_object_or_404(models.Competition, pk=pk)
        if models.CompetitionUser.objects.filter(user_id=request.user, competition_id=competition).exists():
            models.CompetitionUser.objects.filter(
                user_id=request.user, competition_id=competition).delete()
            messages.success(
                request, 'You have successfully unregistered from this competition!')
        else:
            models.CompetitionUser.objects.create(
                user_id=request.user, competition_id=competition)
            messages.success(
                request, 'You have successfully signed up for this competition!')

        return redirect('viewCompetitionDetailed', pk=pk)
