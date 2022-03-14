from django.forms import ModelForm
from .models import FakeMatch, PointSystem

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

class PointSystemForm(ModelForm):
    class Meta:
        model = PointSystem
        fields = ['L_pos1', 'L_pos2', 'L_pos3_4', 'L_pos5_8', 'L_pos9_16', 'L_pos17_32', 'L_pos33_64', 'L_pos65_128', 'L_pos129_256', 
                  'M_pos1', 'M_pos2', 'M_pos3_4', 'M_pos5_8', 'M_pos9_16', 'M_pos17_32', 'M_pos33_64', 'M_pos65_128', 'M_pos129_256',
                  'C_pos1', 'C_pos2', 'C_pos3_4', 'C_pos5_8', 'C_pos9_16', 'C_pos17_32', 'C_pos33_64', 'C_pos65_128', 'C_pos129_256',
                  'F_pos1', 'F_pos2', 'F_pos3_4', 'F_pos5_8', 'F_pos9_16', 'F_pos17_32', 'F_pos33_64', 'F_pos65_128', 'F_pos129_256',
                  'Ladder_pos1', 'Ladder_pos2', 'Ladder_pos3', 'Ladder_pos4', 'Ladder_pos5_8', 'Ladder_pos9_16', 'Ladder_pos17_32', 'Ladder_pos33_64', 'Ladder_pos65_128', 'Ladder_pos129_256',
                  ]