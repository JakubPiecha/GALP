# Generated by Django 4.1.3 on 2022-12-10 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0006_alter_competition_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='type',
            field=models.IntegerField(choices=[(2, 'Cup'), (1, 'League Season')]),
        ),
        migrations.AlterField(
            model_name='match',
            name='away_goal',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='home_goal',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='match_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
