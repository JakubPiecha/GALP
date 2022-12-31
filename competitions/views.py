from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from players.models import Player
from teams.models import Team
from .forms import CompetitionForm, MatchForm
from .models import Competition, Match, PlayerInTeam


class CompetitionListView(ListView):
    '''
    This view is used to display the list of Competitions
    '''
    model = Competition
    template_name = 'competitions/competitions_list.html'
    context_object_name = 'competitions'


class CompetitionDetailView(DetailView):
    '''
    This view to display competitions details
    '''
    model = Competition
    template_name = 'competitions/competitions_detail.html'
    context_object_name = 'competition'


class CompetitionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    '''
    View of the competition creating form
    '''
    form_class = CompetitionForm
    template_name = 'competitions/competition_create.html'
    success_url = reverse_lazy('competitions:competition_list')
    login_url = reverse_lazy('login')
    permission_required = 'competitions.add_competition'


class CompetitionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    '''
    View of the competition edit form
    '''
    form_class = CompetitionForm
    model = Competition
    template_name = 'competitions/competition_edit.html'
    success_url = reverse_lazy('competitions:competition_list')
    login_url = reverse_lazy('competitions:competition_list')
    permission_required = 'competitions.change_competition'


class CompetitionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    '''
    View of the competition delete form
    '''
    model = Competition
    success_url = reverse_lazy('competitions:competition_list')
    login_url = reverse_lazy('competitions:competition_list')
    permission_required = 'competitions.delete_competition'


class CompetitionTeamDetailView(View):
    '''
    view details of the team playing in selected competitions.
    Using this view, we will find out what players are in this team in selected competitions
    '''

    def get(self, request, cpk, tpk):
        players = PlayerInTeam.objects.filter(season_id=cpk, team_id=tpk)
        competition = Competition.objects.get(pk=cpk)
        team = Team.objects.get(pk=tpk)
        return render(
            request,
            "competitions/competitions_team_detail.html",
            context={
                'competition': competition,
                'team': team,
                'players': players,
            })


class MatchScheduleView(DetailView):
    '''
    View of the schedule of selected competitions
    '''
    model = Competition
    template_name = 'competitions/schedule_list.html'
    context_object_name = 'competition'


class MatchCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    '''
    View of the match/game creating form
    '''
    form_class = MatchForm
    login_url = reverse_lazy('competitions:competition_list')
    template_name = 'competitions/add_match.html'
    permission_required = 'competitions.add_match'

    def get_success_url(self, **kwargs):
        return reverse_lazy('competitions:schedule_list', kwargs={'pk': self.object.competition_id})


class MatchUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    '''
    View of the match/game creating form
    '''
    model = Match
    form_class = MatchForm
    login_url = reverse_lazy('competitions:competition_list')
    template_name = 'competitions/edit_match.html'
    permission_required = 'competitions.change_match'

    def get_success_url(self, **kwargs):
        return reverse_lazy('competitions:schedule_list', kwargs={'pk': self.object.competition_id})


class MatchDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    '''
    View of the match/game delete form
    '''
    model = Match
    login_url = reverse_lazy('competitions:competition_list')
    permission_required = 'competitions.delete_match'

    def get_success_url(self, **kwargs):
        return reverse_lazy('competitions:schedule_list', kwargs={'pk': self.object.competition_id})


class CompetitionTableLeagueView(View):
    '''
    view details all teams playing in selected competitions.
    using this view, we create tables with points scored by the team in selected competitions based
    on the results of matches in selected competitions
    '''

    def get(self, request, pk):
        matches = Match.objects.filter(competition_id=pk, home_goal__isnull=False, away_goal__isnull=False)
        competition = Competition.objects.get(pk=pk)
        teams = Team.objects.filter(competition=pk)
        table = {}
        for team in teams:
            table.update({team.team_name: {'games': 0, 'goals scored': 0, 'goals conceded': 0, 'points': 0}})
        for match in matches:
            table[match.home_team.team_name]['games'] += 1
            table[match.away_team.team_name]['games'] += 1
            table[match.home_team.team_name]['goals scored'] += match.home_goal
            table[match.home_team.team_name]['goals conceded'] += match.away_goal
            table[match.away_team.team_name]['goals scored'] += match.away_goal
            table[match.away_team.team_name]['goals conceded'] += match.home_goal
            if match.home_goal > match.away_goal:
                table[match.home_team.team_name]['points'] += 3
            elif match.away_goal > match.home_goal:
                table[match.away_team.team_name]['points'] += 3
            else:
                table[match.away_team.team_name]['points'] += 1
                table[match.home_team.team_name]['points'] += 1
        table_league = sorted(table, key=lambda k: (table[k]['points'], table[k]['goals scored']), reverse=True)
        return render(
            request,
            "competitions/table.html",
            context={
                'competition': competition,
                'teams': teams,
                'table_league': table_league,
                'table': table,
            })
