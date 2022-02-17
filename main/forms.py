from django.forms import ModelForm
from .models import FakeMatch

class FakeMatchForm(ModelForm):
    class Meta:
        model = FakeMatch
        fields = ['points_deduction', 'date', 'team']
        labels = {
            'points_deduction': 'Points to be deducted',
            'date': 'Time of Deduction',
        }