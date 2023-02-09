from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

# Create your models here.


class CustomUser(AbstractUser, PermissionsMixin):
    pass

