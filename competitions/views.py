from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Competition

# Create your views here.


class CompetitionListView(ListView):
    model = Competition
    template_name = 'competitions/competitions_list.html'
    context_object_name = 'competitions'


class CompetitionDetailView(DetailView):
    model = Competition
    template_name = 'competitions/competitions_detail.html'
    context_object_name = 'competition'


class CompetitionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Competition
    fields = ('competition_name', 'teams', 'type', 'owner')
    template_name = 'competitions/competition_create.html'
    success_url = reverse_lazy('competitions:competition_list')
    login_url = reverse_lazy('competitions:competition_list')
    permission_required = 'competition.add_competition'


class CompetitionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Competition
    fields = ('competition_name', 'teams', 'type', 'owner')
    template_name = 'competitions/competition_edit.html'
    success_url = reverse_lazy('competitions:competition_list')
    login_url = reverse_lazy('competitions:competition_list')
    permission_required = 'competition.change_competition'


class CompetitionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Competition
    success_url = reverse_lazy('competitions:competition_list')
    login_url = reverse_lazy('competitions:competition_list')
    permission_required = 'competition.delete_competition'




