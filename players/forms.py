from django import forms
from .models import Player


class PlayerForm(forms.ModelForm):
    date_of_birth = forms.DateField(label='Data urodzenia', widget=forms.DateInput(attrs={'placeholder': 'RRRR-MM-DD'}))

    class Meta:
        model = Player
        fields = ('fullname', 'date_of_birth')
