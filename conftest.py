import pytest
from django.contrib.auth.models import Permission
from django.test import Client

from competitions.models import Competition, Match
from teams.models import Team


@pytest.fixture
def client(user):
    """create django user"""
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def user(db, django_user_model):
    user = django_user_model.objects.create_user(email='test2@admin.com', username='Test User', password='TestPass321')
    permission_add = Permission.objects.get(name='Can add player')
    permission_edit = Permission.objects.get(name='Can change player')
    permission_delete = Permission.objects.get(name='Can delete player')
    permission_add_team = Permission.objects.get(name='Can add team')
    permission_edit_team = Permission.objects.get(name='Can change team')
    permission_delete_team = Permission.objects.get(name='Can delete team')
    user.user_permissions.add(permission_add, permission_edit, permission_delete, permission_edit_team,
                              permission_delete_team, permission_add_team)
    permission_add_competition = Permission.objects.get(name='Can add competition')
    permission_edit_competition = Permission.objects.get(name='Can change competition')
    permission_delete_competition = Permission.objects.get(name='Can delete competition')
    user.user_permissions.add(permission_edit_competition, permission_delete_competition, permission_add_competition)
    permission_add_match = Permission.objects.get(name='Can add match')
    permission_edit_match = Permission.objects.get(name='Can change match')
    permission_delete_match = Permission.objects.get(name='Can delete match')
    user.user_permissions.add(permission_edit_match, permission_delete_match, permission_add_match)
    return user


@pytest.fixture
def user_no_perm(db, django_user_model):
    user = django_user_model.objects.create_user(email='test1@admin.com', username='Test1 User', password='TestPass321')
    return user


@pytest.fixture
def competition(db, user_no_perm):
    team_a = Team.objects.create(team_name='TeamA', owner=user_no_perm)
    team_b = Team.objects.create(team_name='TeamB', owner=user_no_perm)
    teams = Team.objects.all()
    competition = Competition.objects.create(competition_name='test season', owner=user_no_perm)
    competition.teams.set(teams)
    return competition

@pytest.fixture
def team_q(db, user_no_perm):
    team_q = Team.objects.create(team_name='TeamQ', owner=user_no_perm)
    return team_q

@pytest.fixture
def team_w(db, user_no_perm):
    team_w = Team.objects.create(team_name='TeamW', owner=user_no_perm)
    return team_w

@pytest.fixture
def game(db):
    team_o = Team.objects.create(team_name='TeamO')
    team_p = Team.objects.create(team_name='TeamP')
    competition = Competition.objects.create(competition_name='test season 7')
    teams = Team.objects.all()
    competition.teams.set(teams)
    match = Match.objects.create(home_team=team_p, away_team=team_o, competition=competition)
    return match

