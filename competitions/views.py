from django.shortcuts import render
from blog import models
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.


class addCompetition(generic.CreateView):
    model = models.Competition
    fields = ['title', 'location', 'description',
              'category', 'date', 'featuredImage']
    template_name = "Competitions/add_competition.html"
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, 'Competiton created Succesfully')
        return super().form_valid(form)
