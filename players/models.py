from django.db import models


# Create your models here.
class Player(models.Model):
    fullname = models.CharField(max_length=120)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.fullname
