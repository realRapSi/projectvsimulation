from asyncio.windows_events import NULL
from datetime import timedelta
from django.conf import settings
from django.shortcuts import redirect, render
from django.core import files
from .models import Team, Match, FakeMatch
from .forms import FakeMatchForm
import requests
from django.utils import timezone
import json, os
import requests

# Create your views here.
def index(response):
    return render(response, 'main/index.html', {})

def update_database(response):
    #get Teams
    teams = requests.get('https://api.projectv.gg/api/v1/frontend/teams?page_size=10000').json()

    #create Team objects
    for team in teams['data']:
        if not Team.objects.filter(id= team['id']).exists():
            new_team = Team(id = team['id'],
                          name = team['name'], 
                          size = team['members_count'],
                          ladder_points = 1000,
                          projectv_points = 0)
            new_team.save()
    
    #get Matches of Ladder
    matches = requests.get('https://api.projectv.gg/api/v1/frontend/tournaments/fc89fadb-962f-43d5-88c5-4eae082eaf1f/xmatches').json()

    #Create Match objects
    for match in matches:
        if not Match.objects.filter(id= match['id']).exists():
            compute = True
            try:
                teamA = Team.objects.get(id= match['encounters'][0]['participant']['participant']['id'])
            except Team.DoesNotExist:
                teamA = Team.objects.none().first()
                compute = False
            try:
                teamB = Team.objects.get(id= match['encounters'][1]['participant']['participant']['id'])
            except Team.DoesNotExist:
                teamB = Team.objects.none().first()
                compute = False
            new_match = Match(id = match['id'],
                            number = match['number'],
                            status = match['status'],
                            date = match['date'],
                            teamA = teamA,
                            teamB = teamB,
                            teamA_score = match['encounters'][0]['final_score'],
                            teamB_score = match['encounters'][1]['final_score'],
                            match_type = match['round']['group']['name']['en'],
                            compute = compute)
            new_match.save()

    return redirect('/leaderboard')

def run_calculation(response):
    calculation()
    return redirect('/leaderboard')

def ranking(response):
    teams = Team.objects.order_by('-ladder_points')
    return render(response, 'main/index.html', {'teams': teams})

def reset_ladder_points(response):
    teams = Team.objects.all()
    fakematches = FakeMatch.objects.all()
    for team in teams:
        team.ladder_points = 1000
        team.save()
    for match in fakematches:
        match.computed = False
        match.save()
    return redirect('/leaderboard')

def calculation():
    matches = Match.objects.all()
    fake_matches = FakeMatch.objects.all()
    matches_sorted_by_date = matches.order_by('date')

    for match in matches_sorted_by_date:
        if match.compute and match.status == 'COMPLETED':
            for fakematch in fake_matches:
                if match.teamA == fakematch.team:
                    if match.date > fakematch.date and not fakematch.computed:
                        if fakematch.points_deduction_is_reset:
                            match.teamA.ladder_points = 1000
                        elif fakematch.points_deduction_is_multiplier:
                            match.teamA.ladder_points *= fakematch.points_deduction_multiplier
                        fakematch.computed = True
                        fakematch.save()
                        match.teamA.save()
                if match.teamB == fakematch.team:
                    if match.date > fakematch.date and not fakematch.computed:
                        if fakematch.points_deduction_is_reset:
                            match.teamB.ladder_points = 1000
                        elif fakematch.points_deduction_is_multiplier:
                            match.teamB.ladder_points *= fakematch.points_deduction_multiplier
                        fakematch.computed = True
                        fakematch.save()
                        match.teamB.save()

            algorithm(match.teamA, match.teamA_score, match.teamB, match.teamB_score)

def algorithm(tA, tA_score, tB, tB_score):
    fixed_win = 5
    if tA_score == tB_score:
        pass
    else:
        if tA_score > tB_score:
            tA.ladder_points += new1_points_algo(tA.ladder_points, tB.ladder_points) + fixed_win
            tB.ladder_points += -(new1_points_algo(tA.ladder_points, tB.ladder_points)) + fixed_win
        elif tB_score > tA_score:
            tB.ladder_points += new1_points_algo(tB.ladder_points, tA.ladder_points) + fixed_win
            tA.ladder_points += -(new1_points_algo(tB.ladder_points, tA.ladder_points)) + fixed_win
    tA.save()
    tB.save()

def points_deduction(response):

    if response.method == 'POST':
        form = FakeMatchForm(response.POST)
        if form.is_valid():
            new_fakematch = FakeMatch(points_deduction_is_reset=form.cleaned_data['points_deduction_is_reset'],
                                         date=form.cleaned_data['date'],
                                         team=form.cleaned_data['team'],
                                         points_deduction_is_multiplier= form.cleaned_data['points_deduction_is_multiplier'],
                                         points_deduction_muliplier= form.cleaned_data['points_deduction_muliplier'])
            new_fakematch.save()
            return redirect('/pointsdeduction')

    fakematches = FakeMatch.objects.all()
    form = FakeMatchForm()
    return render(response, 'main/fakematches.html', {'fakematches': fakematches, 'form': form})

def current_points_algo(winning_team_ladder_points, losing_team_ladder_points):
    total = winning_team_ladder_points + losing_team_ladder_points
    difference = abs(winning_team_ladder_points - losing_team_ladder_points)

    points_change = int(losing_team_ladder_points/total * 50)

    if points_change < 10:
        return 10
    else:
        return points_change

def new1_points_algo(winning_team_ladder_points, losing_team_ladder_points):

    points_change = int(1/(1+10**((winning_team_ladder_points - losing_team_ladder_points)/400))*50)
    print(points_change)

    return points_change
