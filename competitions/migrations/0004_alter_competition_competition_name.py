# Generated by Django 4.1.3 on 2022-12-08 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='competition_name',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]