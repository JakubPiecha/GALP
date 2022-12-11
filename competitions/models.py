from django.contrib.auth import get_user_model
from django.db import models
from teams.models import Team
from players.models import Player

# Create your models here.


class Competition(models.Model):
    competition_name = models.CharField(max_length=60, unique=True)
    teams = models.ManyToManyField(Team)
    type = models.IntegerField(choices={(1, 'League Season'), (2, 'Cup')})
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.competition_name


class Match(models.Model):
    match_date = models.DateTimeField(blank=True, null=True )
    home_team = models.ForeignKey(Team, related_name='team_home', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='team_away', on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    home_goal = models.IntegerField(blank=True, null=True)
    away_goal = models.IntegerField(blank=True, null=True)


class PlayerInTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.ForeignKey(Competition, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.player.fullname} w rozgrywkach {self.season.competition_name} zgłoszony jest przez {self.team.team_name}'
