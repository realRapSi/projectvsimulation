from django.db import models
from django.forms import CharField, DateTimeField, IntegerField
from django.utils import timezone

# Create your models here.

class Team(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    size = models.IntegerField(blank=True, null=True)
    ladder_points = models.IntegerField(blank=True, null=True)
    projectv_points = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Match(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    number = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(blank=True)
    teamA = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='%(class)s_team_A', blank=True, null=True)
    teamB = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='%(class)s_team_B', blank=True, null=True)
    teamA_score = models.IntegerField(blank=True, null=True)
    teamB_score = models.IntegerField(blank=True, null=True)
    match_type = models.CharField(max_length=200, blank=True)
    compute = models.BooleanField(default=False)

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




