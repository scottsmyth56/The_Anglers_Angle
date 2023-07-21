from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Competition, CompetitionUser, User
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


class viewCompetitions(LoginRequiredMixin, generic.ListView):
    """
    View for displaying a list of competitions.
    """
    model = Competition
    template_name = "Competitions/competitions.html"
    context_object_name = "competitions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class addCompetition(LoginRequiredMixin, generic.CreateView):
    """
    View for adding a new competition.
    """
    model = Competition
    fields = [
        "title",
        "location",
        "description",
        "category",
        "date",
        "featuredImage"]
    template_name = "Competitions/add_competition.html"
    success_url = reverse_lazy("competitions")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, "Competiton created Succesfully")
        return super().form_valid(form)


class viewCompetitionDetailed(LoginRequiredMixin, generic.DetailView):
    """
    View for displaying detailed information about a competition.
    """
    model = Competition
    template_name = "Competitions/competition_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["competition_user"] = CompetitionUser.objects.filter(
            competition_id=self.object, user_id=self.request.user
        )

        context["registered_users"] = User.objects.filter(
            competitionuser__competition_id=self.object
        )

        return context


class enterCompetition(LoginRequiredMixin, generic.CreateView):
    """
    View for entering or leaving a competition.
    """

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        competition = get_object_or_404(Competition, pk=pk)
        if CompetitionUser.objects.filter(
            user_id=request.user, competition_id=competition
        ).exists():
            CompetitionUser.objects.filter(
                user_id=request.user, competition_id=competition
            ).delete()
            messages.success(
                request, "You have successfully unregistered from this competition!")
        else:
            CompetitionUser.objects.create(
                user_id=request.user, competition_id=competition
            )
            messages.success(
                request, "You have successfully signed up for this competition!")

        return redirect("viewCompetitionDetailed", pk=pk)


class editCompetition(LoginRequiredMixin, generic.UpdateView):
    """
    View for editing a competition.
    """
    model = Competition
    fields = [
        "title",
        "location",
        "description",
        "category",
        "date",
        "featuredImage"]
    template_name = "Competitions/edit_competition.html"
    success_url = reverse_lazy("competitions")

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        messages.success(self.request, "Competition updated Succesfully")
        return super().form_valid(form)


class deleteCompetition(LoginRequiredMixin, generic.DeleteView):
    """
    View for deleting a competition.
    """
    model = Competition
    template_name = "Competitions/delete_competition.html"
    success_url = reverse_lazy("competitions")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Competition Deleted Successfully")
        return super().delete(request, *args, **kwargs)
