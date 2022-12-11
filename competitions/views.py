from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from teams.models import Team
from .models import Competition, Match


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


class MatchScheduleView(DetailView):
    model = Competition
    template_name = 'competitions/schedule_list.html'
    context_object_name = 'competition'


class MatchCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Match
    fields = ('match_date', 'home_team', 'away_team', 'competition', 'home_goal', 'away_goal')
    success_url = reverse_lazy('competitions:competition_list')
    login_url = reverse_lazy('competitions:competition_list')
    template_name = 'competitions/add_match.html'
    permission_required = 'competition.add_match'


class MatchUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Match
    fields = ('match_date', 'home_team', 'away_team', 'competition', 'home_goal', 'away_goal')
    success_url = reverse_lazy('competitions:competition_list')
    login_url = reverse_lazy('competitions:competition_list')
    template_name = 'competitions/edit_match.html'
    permission_required = 'competition.change_match'


class MatchDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Match
    success_url = reverse_lazy('competitions:competition_list')
    login_url = reverse_lazy('competitions:competition_list')
    permission_required = 'competition.delete_match'


class CompetitionTableLeagueView(View):

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
