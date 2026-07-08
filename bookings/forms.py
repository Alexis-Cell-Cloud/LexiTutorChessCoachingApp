from django import forms
from .models import Booking, GameType


class BookingForm(forms.ModelForm):
    game = forms.ModelChoiceField(queryset=GameType.objects.all(), empty_label="Select a game")

    class Meta:
        model = Booking
        fields = ['game', 'address', 'session_date', 'session_start_time', 'actual_duration_hours']
        widgets = {
            'session_date': forms.DateInput(attrs={'type': 'date'}),
            'session_start_time': forms.TimeInput(attrs={'type': 'time'}),
        }