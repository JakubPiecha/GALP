from django import forms

from competitions.models import PlayerInTeam
from teams.models import Team


class PlayerInTeamForm(forms.ModelForm):

    class Meta:
        model = PlayerInTeam
        fields = ('team', 'player', 'season')

    def clean(self):
        team = self.cleaned_data['team']
        team = team.id
        player = self.cleaned_data['player']
        player = player.id
        competition = self.cleaned_data['season']
        competition = competition.id
        players = PlayerInTeam.objects.filter(season_id=competition).values_list('player_id', flat=True)
        if player in players:
            raise forms.ValidationError('Zawodnik jest już przypisany w tych rozgrywkach')
        teams = Team.objects.filter(competition=competition).values_list('id', flat=True)
        if team not in teams:
            raise forms.ValidationError('Drużyna nie uczestniczy w tych rozgrywkach')
        return self.cleaned_data


