from django.forms import ModelForm
from .models import FakeMatch

class FakeMatchForm(ModelForm):
    class Meta:
        model = FakeMatch
        fields = ['date', 'team', 'points_deduction_is_reset', 'points_deduction_is_multiplier', 'points_deduction_multiplier']
        labels = {
            'points_deduction_is_reset': 'Points fully reset?',
            'date': 'Time of Deduction',
            'points_deduction_is_multiplier': 'Points partially reset with multiplier?',
            'points_deduction_multiplier': 'Deduction Multiplier (% that remain after deduction): '
        }