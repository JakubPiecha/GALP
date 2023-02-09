from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from pytest_django.asserts import assertTemplateUsed, assertContains, assertNotContains

from competitions.models import Competition, Match
from teams.models import Team
from users.models import CustomUser


class CompetitionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_test = CustomUser.objects.create_user(email='test1@admin.com', username='Test2 User',
                                                   password='TestPass321')
        team_C = Team.objects.create(team_name='TeamC', owner=user_test)
        team_D = Team.objects.create(team_name='TeamD', owner=user_test)
        teams = Team.objects.all()

        cls.competition = Competition.objects.create(competition_name='test season 1', owner=user_test)
        cls.competition.teams.set(teams)

    def test_create_competition_model(self):
        user = CustomUser.objects.create_user(email='test1@admin.com', username='Test1 User',
                                              password='TestPass321')
        team_a = Team.objects.create(team_name='TeamA', owner=user)
        team_b = Team.objects.create(team_name='TeamB', owner=user)
        teams = Team.objects.all()
        competition = Competition.objects.create(competition_name='test season', owner=user)
        competition.teams.set(teams)
        self.assertEqual(competition.competition_name, 'test season')
        self.assertEqual(competition.owner, user)
        self.assertEqual(self.competition.teams.count(), 2)

    def test_competition_listing(self):
        self.assertEqual(f"{self.competition.competition_name}", "test season 1")

    def test_url_template_contains_list_view(self):
        response = self.client.get('/competitions/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'competitions/competitions_list.html')
        self.assertContains(response, 'test season 1')
        self.assertNotContains(response, 'Elo ELo')

    def test_list_view_url_name(self):
        response = self.client.get(reverse('competitions:competition_list'))
        self.assertEqual(response.status_code, 200)

    def test_url_template_contains_detail_view(self):
        response = self.client.get(self.competition.get_absolute_url())
        no_response = self.client.get('/competitions/12354/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'competitions/competitions_detail.html')
        self.assertContains(response, 'test season 1')
        self.assertNotContains(response, 'Elo ELo')


def test_add_competition_get_no_login():
    client = Client()
    response = client.get(reverse('competitions:competition_create'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


def test_add_competition_get_no_perm(user_no_perm):
    client = Client()
    client.force_login(user_no_perm)
    response = client.get(reverse('competitions:competition_create'))
    assert response.status_code == 200
    assert 'Tworzenie rozgrywek' in response.content.decode('UTF-8')


def test_add_competition_post(db, client, user):
    team_a = Team.objects.create(team_name='TeamA', owner=user)
    team_b = Team.objects.create(team_name='TeamB', owner=user)
    data = {'competition_name': 'Season', 'teams': [team_a.id, team_b.id], 'owner': user.id}
    response = client.post(reverse('competitions:competition_create'), data)
    assert Competition.objects.get(competition_name='Season')
    assert response.status_code == 302
    assert response.url.startswith(reverse('competitions:competition_list'))


def test_add_competition_get(client, user):
    response = client.get(reverse('competitions:competition_create'))
    assert 'Tworzenie rozgrywek' in response.content.decode('UTF-8')
    assert response.status_code == 200


def test_edit_competition_get(db, client, user, competition):
    response = client.get(reverse('competitions:competition_edit', kwargs={'pk': competition.id}))
    assert response.status_code == 302
    assert response.url.startswith(reverse('competitions:competition_list'))


def test_edit_competition_get_no_login(db, competition):
    client = Client()
    response = client.get(reverse('competitions:competition_edit', kwargs={'pk': competition.id}))
    assert response.status_code == 302
    assert response.url.startswith(reverse('competitions:competition_list'))


def test_edit_competition_post(db, client, user, competition_user, user_no_perm):
    team_g = Team.objects.create(team_name='TeamG', owner=user_no_perm)
    team_f = Team.objects.create(team_name='TeamF', owner=user_no_perm)
    data = {'competition_name': 'Season', 'teams': [team_g.id, team_f.id], 'owner': user.id}
    response = client.post(reverse('competitions:competition_edit', kwargs={'pk': competition_user.id}), data)
    assert response.status_code == 302
    assert Competition.objects.get(competition_name='Season')
    assert response.url.startswith(reverse('competitions:competition_list'))


def test_edit_competition_get_no_permission(db, user_no_perm, competition):
    client = Client()
    client.force_login(user_no_perm)
    response = client.get(reverse('competitions:competition_edit', kwargs={'pk': competition.id}))
    assert response.status_code == 403
    assert '403 Forbidden' in response.content.decode('UTF-8')


def test_delete_competition_post(db, client, user, competition_user):
    response = client.post(reverse('competitions:competition_delete', kwargs={'pk': competition_user.id}))
    assert response.status_code == 302
    assert list(Competition.objects.all()) == list(Competition.objects.none())
    assert response.url.startswith(reverse('competitions:competition_list'))


def test_delete_competition_post_no_login(db, competition):
    client = Client()
    response = client.post(reverse('competitions:competition_delete', kwargs={'pk': competition.id}))
    assert response.status_code == 302
    assert len(Competition.objects.all().values_list()) == 1
    assert response.url.startswith(reverse('competitions:competition_list'))


def test_delete_competition_post_no_permission(db, user_no_perm, competition):
    client = Client()
    client.force_login(user_no_perm)
    response = client.post(reverse('competitions:competition_delete', kwargs={'pk': competition.id}))
    assert response.status_code == 403
    assert len(Competition.objects.all().values_list()) == 1
    assert '403 Forbidden' in response.content.decode('UTF-8')


def test_schedule_list(db, client, competition):
    url = reverse('competitions:schedule_list', kwargs={'pk': competition.id})
    response = client.get(url)
    assert response.status_code == 200
    assert 'Terminarz rozgrywek:' in response.content.decode('UTF-8')
    assertTemplateUsed(response, 'competitions/schedule_list.html')
    assertContains(response, 'test season')
    assertNotContains(response, 'Elo ELo')


def test_add_match_get_no_login():
    client = Client()
    response = client.get(reverse('competitions:add_match'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('competitions:competition_list'))


def test_add_match_get_no_perm(user_no_perm):
    client = Client()
    client.force_login(user_no_perm)
    response = client.get(reverse('competitions:add_match'))
    assert response.status_code == 403
    assert '403 Forbidden' in response.content.decode('UTF-8')


def test_add_match_post(db, client, user):
    team_x = Team.objects.create(team_name='TeamX', owner=user)
    team_y = Team.objects.create(team_name='TeamY', owner=user)
    teams = Team.objects.all()
    competition = Competition.objects.create(competition_name='season', owner=user)
    competition.teams.set(teams)
    data = {'home_team': team_x.id, 'away_team': team_y.id, 'competition': competition.id}
    response = client.post(reverse('competitions:add_match'), data)
    assert Match.objects.get(competition=competition)
    assert response.status_code == 302
    assert response.url.startswith(reverse('competitions:schedule_list', kwargs={'pk': competition.id}))


def test_add_match_post_this_same_team(db, client, user):
    team_x = Team.objects.create(team_name='TeamX', owner=user)
    teams = Team.objects.all()
    competition = Competition.objects.create(competition_name='season', owner=user)
    competition.teams.set(teams)
    data = {'home_team': team_x.id, 'away_team': team_x.id, 'competition': competition.id}
    response = client.post(reverse('competitions:add_match'), data)
    assert response.status_code == 200
    assert 'Wybrałeś te same drużyny' in response.content.decode('UTF-8')


def test_add_match_post_no_team_in_competiton(db, client, user, competition, team_q, team_w):
    data = {'home_team': team_w.id, 'away_team': team_q.id, 'competition': competition.id}
    response = client.post(reverse('competitions:add_match'), data)
    assert response.status_code == 200
    assert 'Wybrałeś drużynę która nie występuje w tych rozgrywkach' in response.content.decode('UTF-8')


def test_add_match_get(client, user):
    response = client.get(reverse('competitions:add_match'))
    assert 'Dodawanie meczu' in response.content.decode('UTF-8')
    assert response.status_code == 200

def test_edit_match_get_no_login(db, game):
    client = Client()
    response = client.get(reverse('competitions:edit_match', kwargs={'pk': game.id}))
    assert response.status_code == 302
    assert response.url.startswith(reverse('competitions:competition_list'))


def test_edit_match_get_no_perm(db, user_no_perm, game):
    client = Client()
    client.force_login(user_no_perm)
    response = client.get(reverse('competitions:edit_match', kwargs={'pk': game.id}))
    assert response.status_code == 403
    assert '403 Forbidden' in response.content.decode('UTF-8')



def test_edit_match_get(db, client, game):
    response = client.get(reverse('competitions:edit_match', kwargs={'pk': game.id}))
    assert Match.objects.get(id=game.id)
    assert response.status_code == 200


def test_edit_match_post(db, client, user):
    team_x = Team.objects.create(team_name='TeamX', owner=user)
    team_y = Team.objects.create(team_name='TeamY', owner=user)
    teams = Team.objects.all()
    competition = Competition.objects.create(competition_name='season', owner=user)
    competition.teams.set(teams)
    match = Match.objects.create(home_team=team_x, away_team=team_y, competition=competition)
    data = {'home_team': team_y.id, 'away_team': team_x.id, 'competition': competition.id}
    response = client.post(reverse('competitions:edit_match', kwargs={'pk': match.id}), data)
    assert response.status_code == 302
    assert Match.objects.get(home_team=team_y.id)
    assert response.url.startswith(reverse('competitions:schedule_list', kwargs={'pk': competition.id}))

def test_delete_match_post(db, client, user, game):
    response = client.post(reverse('competitions:delete_match', kwargs={'pk': game.id}))
    assert response.status_code == 302
    assert list(Match.objects.all()) == list(Match.objects.none())
    assert response.url.startswith(reverse('competitions:schedule_list', kwargs={'pk': game.competition_id}))


def test_delete_match_post_no_login(db, game):
    client = Client()
    response = client.post(reverse('competitions:delete_match', kwargs={'pk': game.id}))
    assert response.status_code == 302
    assert len(Match.objects.all().values_list()) == 1
    assert response.url.startswith(reverse('competitions:competition_list'))


def test_delete_match_post_no_permission(db, user_no_perm, game):
    client = Client()
    client.force_login(user_no_perm)
    response = client.post(reverse('competitions:delete_match', kwargs={'pk': game.id}))
    assert response.status_code == 403
    assert len(Match.objects.all().values_list()) == 1
    assert '403 Forbidden' in response.content.decode('UTF-8')

def test_table_view(db, client, competition):
    url = reverse('competitions:table', kwargs={'pk': competition.id})
    response = client.get(url)
    assert response.status_code == 200
    assert 'Tabela rozgrywek:' in response.content.decode('UTF-8')
    assertTemplateUsed(response, 'competitions/table.html')
    assertContains(response, 'test season')
    assertNotContains(response, 'Elo Elo')


def test_competition_team_detail_view(db, client, competition):
    team = Team.objects.get(team_name='TeamB')
    url = reverse('competitions:competition_team_detail', kwargs={'cpk': competition.id, 'tpk': team.id})
    response = client.get(url)
    assert response.status_code == 200
    assert 'Lista zgłoszonych zawodników' in response.content.decode('UTF-8')
    assertTemplateUsed(response, 'competitions/competitions_team_detail.html')
    assertContains(response, 'TeamB')
    assertNotContains(response, 'Elo ELo')


