# Generated by Django 4.1.3 on 2022-12-07 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0002_alter_competition_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='type',
            field=models.IntegerField(choices=[(1, 'League Season'), (2, 'Cup')]),
        ),
    ]