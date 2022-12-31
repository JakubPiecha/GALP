import pytest
from django.contrib.auth.models import Permission
from django.test import TestCase, Client
from django.urls import reverse

from players.models import Player


class PlayersTests(TestCase):
    def test_create_player_model(self):
        player = Player.objects.create(fullname='Player Test2', date_of_birth='1999-07-30')
        self.assertEqual(player.fullname, 'Player Test2')
        self.assertEqual(player.date_of_birth, '1999-07-30')


    @classmethod
    def setUpTestData(cls):
        cls.player = Player.objects.create(fullname='Player Test', date_of_birth='1999-07-31')

    def test_players_listing(self):
        self.assertEqual(f"{self.player.fullname}", "Player Test")
        self.assertEqual(f"{self.player.date_of_birth}", "1999-07-31")

    def test_url_template_contains_list_view(self):
        response = self.client.get('/players/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'players/players_list.html')
        self.assertContains(response, 'Player Test')
        self.assertNotContains(response, 'Elo ELo')

    def test_list_view_url_name(self):
        response = self.client.get(reverse('players:player_list'))
        self.assertEqual(response.status_code, 200)

    def test_url_template_contains_detail_view(self):
        response = self.client.get(self.player.get_absolute_url())
        no_response = self.client.get('/players/12354/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'players/player_detail.html')
        self.assertContains(response, 'Player Test')
        self.assertNotContains(response, 'Elo ELo')

    def test_detail_view_url_name(self):
        response = self.client.get(reverse('players:player_detail', kwargs={'pk': self.player.id}))
        self.assertEqual(response.status_code, 200)


def test_create_player_get_no_login():
    client = Client()
    response = client.get(reverse('players:player_add'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('players:player_list'))

def test_add_palyer_get_no_perm(user_no_perm):
    client = Client()
    client.force_login(user_no_perm)
    response = client.get(reverse('players:player_add'))
    assert response.status_code == 403
    assert '403 Forbidden' in response.content.decode('UTF-8')

@pytest.mark.django_db
def test_add_player_post(client, user):
    data = {'fullname': 'PlayerTest2', 'date_of_birth': '1999-07-30'}
    response = client.post(reverse('players:player_add'), data)
    assert Player.objects.get(fullname='PlayerTest2')
    assert response.status_code == 302
    assert response.url.startswith(reverse('players:player_list'))


def test_add_player_get(client, user):
    response = client.get(reverse('players:player_add'))
    assert 'Dodawanie Zawodnika' in response.content.decode('UTF-8')
    assert response.status_code == 200

def test_edit_player_post(db, client, user):
    player = Player.objects.create(fullname='Player Test2', date_of_birth='1999-07-30')
    response = client.post(reverse('players:player_edit', kwargs={'pk': player.id}),
        {'fullname': 'Player Test3', 'date_of_birth': '1998-07-29'})
    assert response.status_code == 302
    assert Player.objects.get(fullname='Player Test3')
    assert response.url.startswith(reverse('players:player_list'))

def test_edit_player_get(db, client, user):
    player = Player.objects.create(fullname='Player Test2', date_of_birth='1999-07-30')
    response = client.get(reverse('players:player_edit', kwargs={'pk': player.id}))
    assert response.status_code == 200
    assert 'Player Test2' in str(response.content)


def test_edit_player_get_no_login(db):
    client = Client()
    player = Player.objects.create(fullname='Player Test2', date_of_birth='1999-07-30')
    response = client.get(reverse('players:player_edit', kwargs={'pk': player.id}))
    assert response.status_code == 302
    assert response.url.startswith(reverse('players:player_list'))

def test_edit_player_get_no_permision(db, user_no_perm):
    client = Client()
    client.force_login(user_no_perm)
    player = Player.objects.create(fullname='Player Test2', date_of_birth='1999-07-30')
    response = client.get(reverse('players:player_edit', kwargs={'pk': player.id}))
    assert response.status_code == 403
    assert '403 Forbidden' in response.content.decode('UTF-8')

def test_delete_player_post(db, client, user):
    player = Player.objects.create(fullname='Player Test2', date_of_birth='1999-07-30')
    response = client.post(reverse('players:player_delete', kwargs={'pk': player.id}))
    assert response.status_code == 302
    assert list(Player.objects.all()) == list(Player.objects.none())
    assert response.url.startswith(reverse('players:player_list'))

def test_delete_player_post_no_login(db, user_no_perm):
    client = Client()
    player = Player.objects.create(fullname='Player Test2', date_of_birth='1999-07-30')
    response = client.post(reverse('players:player_delete', kwargs={'pk': player.id}))
    assert response.status_code == 302
    assert len(Player.objects.all().values_list()) == 1
    assert response.url.startswith(reverse('players:player_list'))

def test_delete_player_post_no_perm(db, user_no_perm):
    client = Client()
    client.force_login(user_no_perm)
    player = Player.objects.create(fullname='Player Test2', date_of_birth='1999-07-30')
    response = client.post(reverse('players:player_delete', kwargs={'pk': player.id}))
    assert response.status_code == 403
    assert len(Player.objects.all().values_list()) == 1
    assert '403 Forbidden' in response.content.decode('UTF-8')






