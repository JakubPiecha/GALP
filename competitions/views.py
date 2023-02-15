import os
from random import shuffle
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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


class CompetitionCreateView(LoginRequiredMixin, CreateView):
    '''
    View of the competition creating form
    '''
    form_class = CompetitionForm
    success_url = reverse_lazy('competitions:competition_list')
    template_name = 'competitions/competition_create.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = get_user_model().objects.get(username=self.request.user)
        group = Group.objects.get(name=os.environ.get('DJ_GROUP_COMPETITION_OWNER'))
        user.groups.add(group)
        self.object.owner = self.request.user
        self.object.save()
        return super(CompetitionCreateView, self).form_valid(form)


class CompetitionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    '''
    View of the competition edit form
    '''
    fields = ('competition_name', 'teams', 'owner')
    model = Competition
    template_name = 'competitions/competition_edit.html'
    success_url = reverse_lazy('competitions:competition_list')
    login_url = reverse_lazy('competitions:competition_list')
    permission_required = 'competitions.change_competition'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner == self.request.user or self.request.user.is_staff:
            return super(CompetitionUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'Tylko właściciel lub administrator może edytować rozgrywki!')
            return redirect('competitions:competition_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if form.cleaned_data['owner']:
            group = Group.objects.get(name=os.environ.get('DJ_GROUP_COMPETITION_OWNER'))
            user = get_user_model().objects.get(username=form.cleaned_data['owner'])
            user.groups.add(group)
        self.object.save()
        return super(CompetitionUpdateView, self).form_valid(form)


class CompetitionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    '''
    View of the competition delete form
    '''
    model = Competition
    success_url = reverse_lazy('competitions:competition_list')
    login_url = reverse_lazy('competitions:competition_list')
    permission_required = 'competitions.delete_competition'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner == self.request.user or self.request.user.is_staff:
            return super(CompetitionDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'Tylko właściciel lub administrator może usunąć rozgrywki!')
            return redirect('competitions:competition_list')


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

    def post(self, request, pk):
        teams = list(Team.objects.filter(competition=pk).values_list('id', flat=True))
        shuffle(teams)
        if len(teams) % 2 != 0:
            teams.append(-1)
        if 'one_round' in request.POST:
            if len(Match.objects.filter(competition_id=pk)) == 0:
                create_schedule_one_round(teams, pk)
            else:
                type_schedule = 'one_round'
                request.session['type_schedule'] = type_schedule
                return redirect('competitions:competition_confirm', pk)
            return redirect('competitions:schedule_list', pk)
        elif 'two_round' in request.POST:
            if len(Match.objects.filter(competition_id=pk)) == 0:
                create_schedule_two_round(teams, pk)
            else:
                type_schedule = 'two_round'
                request.session['type_schedule'] = type_schedule
                return redirect('competitions:competition_confirm', pk)
            return redirect('competitions:schedule_list', pk)


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
# TODO default tournament name and team filter and add more statistic to game (player score, cards etc.)

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
# TODO add more statistic to table

class ConfirmView(View):

    def get(self, request, pk):
        competition = Competition.objects.get(id=pk)
        return render(request, 'competitions/schedule_confirm.html', context={'competition': competition})

    def post(self, request, pk):
        teams = list(Team.objects.filter(competition=pk).values_list('id', flat=True))
        shuffle(teams)
        if len(teams) % 2 != 0:
            teams.append(-1)
        Match.objects.filter(competition_id=pk).delete()
        if request.session['type_schedule'] == 'one_round':
            create_schedule_one_round(teams, pk)
        elif request.session['type_schedule'] == 'two_round':
            create_schedule_two_round(teams, pk)
        return redirect('competitions:schedule_list', pk)


def next_move(teams):
    return [teams[0]] + [teams[-1]] + teams[1:-1]


def create_match_a(teams, pk):
    round = list(zip(teams[:len(teams) // 2], teams[-1:len(teams) // 2 - 1:-1]))
    for game in round:
        if game[0] != -1 and game[1] != -1:
            Match.objects.create(home_team_id=game[0], away_team_id=game[1], competition_id=pk)


def create_match_b(teams, pk):
    round = list(zip(teams[-1:len(teams) // 2 - 1:-1], teams[:len(teams) // 2]))
    for game in round:
        if game[0] != -1 and game[1] != -1:
            Match.objects.create(home_team_id=game[0], away_team_id=game[1], competition_id=pk)


def create_schedule_one_round(teams, pk):
    for games in range(len(teams) // 2):
        if games < len(teams) // 2 - 1:
            create_match_a(teams, pk)
            teams = next_move(teams)
            create_match_b(teams, pk)
            teams = next_move(teams)
        else:
            create_match_a(teams, pk)


def create_schedule_two_round(teams, pk):
    for games in range(len(teams) - 1):
        create_match_b(teams, pk)
        teams = next_move(teams)
        create_match_a(teams, pk)
        teams = next_move(teams)
