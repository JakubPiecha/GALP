from django.db import models
from django.urls import reverse


# Create your models here.
class Player(models.Model):
    fullname = models.CharField(max_length=120)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.fullname

    def get_absolute_url(self):
        return reverse('players:player_detail', args=[str(self.id)])
