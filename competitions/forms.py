from django import forms

from teams.models import Team
from .models import Competition, Match


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ('competition_name', 'teams',)


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('match_date', 'home_team', 'away_team', 'competition', 'home_goal', 'away_goal')




    def clean(self):
        team_home = self.cleaned_data['home_team']
        team_away = self.cleaned_data['away_team']
        teams = Team.objects.filter(competition=self.cleaned_data['competition'])
        if team_home not in teams or team_away not in teams:
            raise forms.ValidationError('Wybrałeś drużynę która nie występuje w tych rozgrywkach')
        if team_home == team_away:
            raise forms.ValidationError('Wybrałeś te same drużyny')
        return self.cleaned_data
