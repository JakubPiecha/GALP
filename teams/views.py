from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from teams.models import Team


# Create your views here.
class TeamsListView(ListView):
    model = Team
    template_name = 'teams/teams_list.html'
    context_object_name = 'teams'


class TeamCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Team
    fields = ('team_name', 'owner', )
    template_name = 'teams/teams_add.html'
    success_url = reverse_lazy('teams:teams_list')
    login_url = reverse_lazy('teams:teams_list')
    permission_required = 'team.add_team'


class TeamDetailView(DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'


class TeamUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Team
    fields = ('team_name', 'owner')
    template_name = 'teams/team_edit.html'
    success_url = reverse_lazy('teams:teams_list')
    login_url = reverse_lazy('teams:teams_list')
    permission_required = 'team.change_team'


class TeamDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Team
    success_url = reverse_lazy('teams:teams_list')
    login_url = reverse_lazy('teams:teams_list')
    permission_required = 'team.delete_team'



