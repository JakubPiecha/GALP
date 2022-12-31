from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from teams.forms import PlayerInTeamForm
from teams.models import Team
from competitions.models import PlayerInTeam


class TeamsListView(ListView):
    '''
    This view is used to display the list of teams
    '''
    model = Team
    template_name = 'teams/teams_list.html'
    context_object_name = 'teams'


class TeamCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    '''
    View of the team creating form
    '''
    model = Team
    fields = ('team_name', 'owner',)
    template_name = 'teams/teams_add.html'
    success_url = reverse_lazy('teams:teams_list')
    login_url = reverse_lazy('login')
    permission_required = 'teams.add_team'


class TeamDetailView(DetailView):
    '''
    This view is used to display team details
    '''
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'teams'


class TeamUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    '''
    View of the team editing form
    '''
    model = Team
    fields = ('team_name', 'owner')
    template_name = 'teams/team_edit.html'
    success_url = reverse_lazy('teams:teams_list')
    login_url = reverse_lazy('teams:teams_list')
    permission_required = 'teams.change_team'


class TeamDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    '''
    View of the delete team
    '''
    model = Team
    success_url = reverse_lazy('teams:teams_list')
    login_url = reverse_lazy('teams:teams_list')
    permission_required = 'teams.delete_team'


class AddPlayerToTeam(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    '''
    View of the form adding a player to the team in specific competitions
    '''

    form_class = PlayerInTeamForm
    template_name = 'teams/add_player_team.html'
    login_url = reverse_lazy('login')
    permission_required = 'competitions.add_playerinteam'

    def get_success_url(self, **kwargs):
        return reverse_lazy('teams:team_detail', kwargs={'pk': self.object.team_id})


class DeletePlayerForTeamView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    '''
     View deleting a player to the team in specific competitions
    '''
    model = PlayerInTeam
    login_url = reverse_lazy('teams:teams_list')
    permission_required = 'competitions.delete_playerinteam'

    def get_success_url(self, **kwargs):
        return reverse_lazy('teams:team_detail', kwargs={'pk': self.object.team_id})
