from django.db import models
from django.utils import timezone

# Create your models here.

class Team(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    size = models.IntegerField(blank=True, null=True)
    ladder_points = models.IntegerField(blank=True, null=True)
    projectv_points = models.IntegerField(blank=True, null=True)
    last_game = models.DateTimeField(blank=True, default=timezone.now)

    def __str__(self) -> str:
        return self.name


class Match(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    type = models.CharField(max_length=200, default='')
    number = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(blank=True)
    teamA = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='%(class)s_team_A', blank=True, null=True)
    teamB = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='%(class)s_team_B', blank=True, null=True)
    teamA_score = models.IntegerField(default=0)
    teamB_score = models.IntegerField(default=0)
    match_type = models.CharField(max_length=200, blank=True)
    compute = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return str(self.teamA) + ' vs. ' + str(self.teamB)

class FakeMatch(models.Model):
    id = models.AutoField(primary_key=True)
    compute = models.BooleanField(default=False)
    computed = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    points_deduction_is_reset = models.BooleanField(default=False)
    points_deduction_is_multiplier = models.BooleanField(default=False)
    points_deduction_multiplier = models.FloatField(blank=True, null=True, default=1.00)
    date = models.DateTimeField(blank=False, default=timezone.now)


    def __str__(self) -> str:
        return self.team.name

class PointSystem(models.Model):
    L_pos1 = models.IntegerField(default=0)
    L_pos2 = models.IntegerField(default=0)
    L_pos3_4 = models.IntegerField(default=0)
    L_pos5_8 = models.IntegerField(default=0)
    L_pos9_16 = models.IntegerField(default=0)
    L_pos17_32 = models.IntegerField(default=0)
    L_pos33_64 = models.IntegerField(default=0)
    L_pos65_128 = models.IntegerField(default=0)
    L_pos129_256 = models.IntegerField(default=0)
    L_pos257_512 = models.IntegerField(default=0)
    L_win = models.IntegerField(default=0)
    L_loss = models.IntegerField(default=0)
    
    M_pos1 = models.IntegerField(default=0)
    M_pos2 = models.IntegerField(default=0)
    M_pos3_4 = models.IntegerField(default=0)
    M_pos5_8 = models.IntegerField(default=0)
    M_pos9_16 = models.IntegerField(default=0)
    M_pos17_32 = models.IntegerField(default=0)
    M_pos33_64 = models.IntegerField(default=0)
    M_pos65_128 = models.IntegerField(default=0)
    M_pos129_256 = models.IntegerField(default=0)
    M_pos257_512 = models.IntegerField(default=0)
    M_win = models.IntegerField(default=0)
    M_loss = models.IntegerField(default=0)
    
    C_pos1 = models.IntegerField(default=0)
    C_pos2 = models.IntegerField(default=0)
    C_pos3_4 = models.IntegerField(default=0)
    C_pos5_8 = models.IntegerField(default=0)
    C_pos9_16 = models.IntegerField(default=0)
    C_pos17_32 = models.IntegerField(default=0)
    C_pos33_64 = models.IntegerField(default=0)
    C_pos65_128 = models.IntegerField(default=0)
    C_pos129_256 = models.IntegerField(default=0)
    C_pos257_512 = models.IntegerField(default=0)
    C_win = models.IntegerField(default=0)
    C_loss = models.IntegerField(default=0)
    
    F_pos1 = models.IntegerField(default=0)
    F_pos2 = models.IntegerField(default=0)
    F_pos3_4 = models.IntegerField(default=0)
    F_pos5_8 = models.IntegerField(default=0)
    F_pos9_16 = models.IntegerField(default=0)
    F_pos17_32 = models.IntegerField(default=0)
    F_pos33_64 = models.IntegerField(default=0)
    F_pos65_128 = models.IntegerField(default=0)
    F_pos129_256 = models.IntegerField(default=0)
    F_pos257_512 = models.IntegerField(default=0)
    F_win = models.IntegerField(default=0)
    F_loss = models.IntegerField(default=0)
    
    Ladder_pos1 = models.IntegerField(default=0)
    Ladder_pos2 = models.IntegerField(default=0)
    Ladder_pos3 = models.IntegerField(default=0)
    Ladder_pos4 = models.IntegerField(default=0)
    Ladder_pos5_8 = models.IntegerField(default=0)
    Ladder_pos9_16 = models.IntegerField(default=0)
    Ladder_pos17_32 = models.IntegerField(default=0)
    Ladder_pos33_64 = models.IntegerField(default=0)
    Ladder_pos65_128 = models.IntegerField(default=0)
    Ladder_pos129_256 = models.IntegerField(default=0)
    Ladder_pos257_512 = models.IntegerField(default=0)
    Ladder_win = models.IntegerField(default=0)
    Ladder_loss = models.IntegerField(default=0)

