# Generated by Django 4.1.3 on 2022-12-09 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]
