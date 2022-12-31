from django import forms

from teams.models import Team
from .models import Player


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('fullname', 'date_of_birth')
