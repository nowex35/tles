# forms.py
from django import forms
from .models import Event

class UploadCSVForm(forms.Form):
    file = forms.FileField(label="CSVファイル")

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'team_name', 
            'opponent_team', 
            'game_date', 
            'opening_time', 
            'event_place', 
            'release_date', 
            'number_of_spectators', 
            'event_image', 
            'description'
        ]
        widgets = {
            'game_date': forms.DateInput(attrs={'type': 'date'}),
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }