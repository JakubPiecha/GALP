from django.contrib.auth import get_user_model
from django.db import models
from teams.models import Team
# Create your models here.


class Player(models.Model):
    fullname = models.CharField(max_length=120)
    date_of_birth = models.DateTimeField()

    def __str__(self):
        return self.fullname


class Competition(models.Model):
    competition_name = models.CharField(max_length=60, unique=True)
    teams = models.ManyToManyField(Team)
    type = models.IntegerField(choices={(1, 'League Season'), (2, 'Cup')})
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.competition_name


class Match(models.Model):
    match_date = models.DateTimeField()
    home_team = models.ForeignKey(Team, related_name='team_home', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='team_away', on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    home_goal = models.IntegerField(null=True)
    away_goal = models.IntegerField(null=True)


class PlayerInTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.ForeignKey(Competition, on_delete=models.CASCADE)
