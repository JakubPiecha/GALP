# Generated by Django 4.1.3 on 2023-02-08 09:28
import os

from django.db import migrations

def create_superuser(apps, schema_editor):
    User = apps.get_model('users.CustomUser')

    DJ_SU_USERNAME = os.environ.get('DJ_SU_USERNAME')
    DJ_SU_PASSWORD = os.environ.get('DJ_SU_PASSWORD')


    User.objects.create_superuser(
        username=DJ_SU_USERNAME,
        password=DJ_SU_PASSWORD
    )

def delete_superuser(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser, delete_superuser)
    ]
