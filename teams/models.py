from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class Team(models.Model):
    team_name = models.CharField(max_length=60, unique=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.team_name
