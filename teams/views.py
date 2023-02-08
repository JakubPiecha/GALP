import os

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
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


class TeamCreateView(LoginRequiredMixin, CreateView):
    '''
    View of the team creating form
    '''
    model = Team
    fields = ('team_name',)
    template_name = 'teams/teams_add.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        user = get_user_model().objects.get(username=self.request.user)
        group = Group.objects.get(name=os.environ.get('DJ_GROUP_TEAM_OWNER'))
        user.groups.add(group)
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return redirect(reverse_lazy('teams:teams_list'))


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

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner == self.request.user or self.request.user.is_staff:
            return super(TeamUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'Tylko właściciel lub administrator może edytować zespół!')
            return redirect('teams:teams_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = get_user_model().objects.get(username=form.cleaned_data['owner'])
        group = Group.objects.get(name=os.environ.get('DJ_GROUP_TEAM_OWNER'))
        user.groups.add(group)
        self.object.save()
        return redirect(reverse_lazy('teams:teams_list'))


class TeamDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    '''
    View of the delete team
    '''
    model = Team
    success_url = reverse_lazy('teams:teams_list')
    login_url = reverse_lazy('teams:teams_list')
    permission_required = 'teams.delete_team'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner == self.request.user or self.request.user.is_staff:
            return super(TeamDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'Tylko właściciel lub administrator może usunąć zespół!')
            return redirect('teams:teams_list')


class AddPlayerToTeam(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    '''
    View of the form adding a player to the team in specific competitions
    '''

    form_class = PlayerInTeamForm
    template_name = 'teams/add_player_team.html'
    login_url = reverse_lazy('login')
    permission_required = 'competitions.add_playerinteam'

    def get_form_kwargs(self):
        kwargs = super(AddPlayerToTeam, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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
