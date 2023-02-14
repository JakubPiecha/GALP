from django import forms

from competitions.models import PlayerInTeam, Competition
from teams.models import Team


class PlayerInTeamForm(forms.ModelForm):

    class Meta:
        model = PlayerInTeam
        fields = ('team', 'player', 'season')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PlayerInTeamForm, self).__init__(*args, **kwargs)
        if not user.is_staff:
            if len(Competition.objects.filter(owner=user)) == 0:
                self.fields['team'].queryset = Team.objects.filter(owner=user)
                self.fields['season'].queryset = Competition.objects.filter(teams__in=Team.objects.filter(owner=user))
            else:
                self.fields['team'].queryset = Team.objects.filter(competition__owner_id=user).distinct()
                self.fields['season'].queryset = Competition.objects.filter(owner=user)

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


