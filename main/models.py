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




