
from django.test import TestCase, Client
from django.urls import reverse

from teams.models import Team
from users.models import CustomUser


class TeamsTests(TestCase):

    def test_create_team_model(self):
        user = CustomUser.objects.create_user(email='test1@admin.com', username='Test1 User',
                                              password='TestPass321')
        team = Team.objects.create(team_name='TeamB', owner=user)
        self.assertEqual(team.team_name, 'TeamB')
        self.assertEqual(team.owner, user)

    @classmethod
    def setUpTestData(cls):
        cls.team = Team.objects.create(team_name='TeamA')

    def test_teams_listing(self):
        self.assertEqual(f"{self.team.team_name}", "TeamA")

    def test_url_template_contains_list_view(self):
        response = self.client.get('/teams/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams/teams_list.html')
        self.assertContains(response, 'TeamA')
        self.assertNotContains(response, 'Elo ELo')

    def test_list_view_url_name(self):
        response = self.client.get(reverse('teams:teams_list'))
        self.assertEqual(response.status_code, 200)

    def test_url_template_contains_detail_view(self):
        response = self.client.get(self.team.get_absolute_url())
        no_response = self.client.get('/teams/12354/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'teams/team_detail.html')
        self.assertContains(response, 'TeamA')
        self.assertNotContains(response, 'Elo ELo')


def test_add_team_get_no_login():
    client = Client()
    response = client.get(reverse('teams:team_add'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


def test_add_team_get_no_perm(user_no_perm):
    client = Client()
    client.force_login(user_no_perm)
    response = client.get(reverse('teams:team_add'))
    assert response.status_code == 200
    assert 'Dodawanie Zespołu' in response.content.decode('UTF-8')


def test_add_team_post(db, client, user):
    data = {'team_name': 'TeamB', 'owner': user.id}
    response = client.post(reverse('teams:team_add'), data)
    assert Team.objects.get(team_name='TeamB', owner=user.id)
    assert response.status_code == 302
    assert response.url.startswith(reverse('teams:teams_list'))


def test_add_team_get(client, user):
    response = client.get(reverse('teams:team_add'))
    assert 'Dodawanie Zespołu' in response.content.decode('UTF-8')
    assert response.status_code == 200


def test_edit_team_post(db, user, client):
    team = Team.objects.create(team_name='TeamA', owner=user)
    response = client.post(reverse('teams:team_edit', kwargs={'pk': team.id}),
                           {'team_name': 'TeamZ'})
    assert response.status_code == 302
    assert Team.objects.get(team_name='TeamZ')
    assert response.url.startswith(reverse('teams:teams_list'))


def test_edit_team_get(db, client, user):
    team = Team.objects.create(team_name='TeamA', owner=user)
    response = client.get(reverse('teams:team_edit', kwargs={'pk': team.id}))
    assert response.status_code == 200
    assert 'TeamA' in str(response.content)


def test_edit_team_get_no_login(db):
    client = Client()
    team = Team.objects.create(team_name='TeamA')
    response = client.get(reverse('teams:team_edit', kwargs={'pk': team.id}))
    assert response.status_code == 302
    assert response.url.startswith(reverse('teams:teams_list'))


def test_edit_team_get_no_permission(db, user_no_perm, user):
    client = Client()
    client.force_login(user_no_perm)
    team = Team.objects.create(team_name='TeamA', owner=user)
    response = client.get(reverse('teams:team_edit', kwargs={'pk': team.id}))
    assert response.status_code == 302
    assert response.url.startswith(reverse('teams:teams_list'))


def test_delete_team_post(db, client, user):
    team = Team.objects.create(team_name='TeamA', owner=user)
    response = client.post(reverse('teams:team_delete', kwargs={'pk': team.id}))
    assert response.status_code == 302
    assert list(Team.objects.all()) == list(Team.objects.none())
    assert response.url.startswith(reverse('teams:teams_list'))


def test_delete_team_post_no_login(db, user_no_perm):
    client = Client()
    team = Team.objects.create(team_name='TeamA', owner=user_no_perm)
    response = client.post(reverse('teams:team_delete', kwargs={'pk': team.id}))
    assert response.status_code == 302
    assert len(Team.objects.all().values_list()) == 1
    assert response.url.startswith(reverse('teams:teams_list'))


def test_delete_team_post_no_permission(db, user_no_perm):
    client = Client()
    client.force_login(user_no_perm)
    team = Team.objects.create(team_name='TeamA', owner=user_no_perm)
    response = client.post(reverse('teams:team_delete', kwargs={'pk': team.id}))
    assert response.status_code == 403
    assert len(Team.objects.all().values_list()) == 1
    assert '403 Forbidden' in response.content.decode('UTF-8')
