# Generated by Django 4.1.3 on 2022-12-08 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
        ('competitions', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='competition',
            name='teams',
            field=models.ManyToManyField(to='teams.team'),
        ),
    ]
