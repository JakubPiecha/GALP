from django.contrib.auth import get_user_model
from django.db import models
from teams.models import Team
from players.models import Player


# Create your models here.


class Competition(models.Model):
    competition_name = models.CharField(max_length=60, verbose_name='Nazwa Rozgrywek', unique=True)
    teams = models.ManyToManyField(Team, verbose_name='Uczestnicy')
    owner = models.ForeignKey(get_user_model(), verbose_name='Właściciel', on_delete=models.CASCADE, null=True,
                              blank=True)

    def __str__(self):
        return self.competition_name


class Match(models.Model):
    match_date = models.DateTimeField(blank=True, null=True, verbose_name='Data meczu')
    home_team = models.ForeignKey(Team, related_name='team_home', on_delete=models.CASCADE,
                                  verbose_name='Drużyna gospodarzy')
    away_team = models.ForeignKey(Team, related_name='team_away', on_delete=models.CASCADE,
                                  verbose_name='Drużyna gości')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name='Rozgrywki')
    home_goal = models.PositiveIntegerField(blank=True, null=True, verbose_name='Bramki gospodarzy')
    away_goal = models.PositiveIntegerField(blank=True, null=True, verbose_name='Bramki gości')


class PlayerInTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Zespół w którym występuje:')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Nazwa zawodnika:')
    season = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name='W rozgrywkach:' )
    #
    # def __str__(self):
    #     return f'{self.player.fullname} w rozgrywkach {self.season.competition_name} zgłoszony jest przez {self.team.team_name}'
