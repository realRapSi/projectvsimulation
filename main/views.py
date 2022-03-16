from asyncio.windows_events import NULL
from datetime import timedelta
from django.shortcuts import redirect, render
from django.forms.models import model_to_dict
from .models import PointSystem, Team, LadderMatch, FakeMatch, Tournament, Result
from .forms import FakeMatchForm, PointSystemForm, TournamentForm
import requests
from django.utils import timezone
import json, os
import requests
import datetime as dt

# Create your views here.
def update_database(response):
    #get Teams
    teams = requests.get('https://api.projectv.gg/api/v1/frontend/teams?page_size=100000').json()

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
    matches = requests.get('https://api.projectv.gg/api/v1/frontend/tournaments/fc89fadb-962f-43d5-88c5-4eae082eaf1f/xmatches').json()['data']

    #Create Match objects
    for match in matches:
        if not LadderMatch.objects.filter(id= match['id']).exists():
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
            new_match = LadderMatch(id = match['id'],
                            type = 'LADDER',
                            number = match['number'],
                            status = match['status'],
                            date = match['date'],
                            teamA = teamA,
                            teamB = teamB,
                            teamA_score = match['encounters'][0]['final_score'],
                            teamB_score = match['encounters'][1]['final_score'],
                            match_type = match['round']['group']['stage']['name']['de'],
                            compute = compute)
            new_match.save()
    
    #tournaments and results
    tours = requests.get('https://api.projectv.gg/api/v1/frontend/tournaments').json()['data']
    
    for tour in tours:
        if not Tournament.objects.filter(id=tour['id']):
            tour_obj = Tournament(id=tour['id'], name=tour['name']['de'], type='')
            tour_obj.save()
        tournament_obj = Tournament.objects.get(id=tour['id'])
        if not tournament_obj.id == 'fc89fadb-962f-43d5-88c5-4eae082eaf1f':
            tournament_results(tournament_obj)
        
    
    return redirect('leaderboard')

def run_calculation(response):
    teams = Team.objects.all()
    calc_settings = PointSystem.objects.first()
    for team in teams:
        team.projectv_points = 0
        if calc_settings.recalculate_ladder:
            team.ladder_points = 1000
            team.ladder_wins = 0
            team.ladder_loss = 0
            team.ladder_rank = None
        team.save()
        
    if calc_settings.recalculate_ladder:
        calc_settings.ladder_calculated = False
        ladder_calculation()
        calc_settings.ladder_calculated = True
        calc_settings.recalculate_ladder = False
        calc_settings.save()
        
    vrc_calculation()
    
    return redirect('leaderboard')

def ranking(response):
    teams = Team.objects.order_by('-projectv_points')
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
    return redirect('')

def ladder_calculation():
    matches_sorted_by_date = LadderMatch.objects.all().order_by('date')
    fake_matches = FakeMatch.objects.all()

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

    ladder_ranking() 
    
def vrc_calculation(): 
    results = Result.objects.all()
    points = PointSystem.objects.first()
        
    point_dict = model_to_dict(points)
    point_distribution = {}
    for key,value in point_dict.items():
        point_distribution[key.replace('_', '-')] = value
        
    for result in results:
        if result.place == '3' or result.place == '4':
            result.place = '3-4'
            result.save()
        if result.place == None:
            continue
        matching_key = str(result.tournament.type[0]) + '-pos' + str(result.place)
        result.team.projectv_points += point_distribution[matching_key]
        result.team.save()
    if points.ladder_calculated:
        teams = Team.objects.all()
        
        for team in teams:
            ladder_matching_key = ''
            if team.ladder_rank <=4:
                ladder_matching_key = 'Ladder-pos' + str(team.ladder_rank)
            elif team.ladder_rank > 4 and team.ladder_rank <= 8:
                ladder_matching_key = 'Ladder-pos' + str('5-8')
            elif team.ladder_rank > 8 and team.ladder_rank <= 16:
                ladder_matching_key = 'Ladder-pos' + str('9-16')
            elif team.ladder_rank > 16 and team.ladder_rank <= 32:
                ladder_matching_key = 'Ladder-pos' + str('17-32')
            elif team.ladder_rank > 32 and team.ladder_rank <= 64:
                ladder_matching_key = 'Ladder-pos' + str('33-64')
            elif team.ladder_rank > 64 and team.ladder_rank <= 128:
                ladder_matching_key = 'Ladder-pos' + str('65-128') 
            elif team.ladder_rank > 128 and team.ladder_rank <= 256:
                ladder_matching_key = 'Ladder-pos' + str('129-256')
            
            if ladder_matching_key:
                team.projectv_points += point_distribution[ladder_matching_key]
                team.save()

def algorithm(tA, tA_score, tB, tB_score):
    pointsSystem = PointSystem.objects.get(id=1)
    if tA_score == tB_score:
        pass
    if not tA_score == tB_score and not tA_score == None and not tB_score == None:
        if pointsSystem.algo:
            if tA_score > tB_score:
                tA.ladder_points += new1_points_algo(tA.ladder_points, tB.ladder_points) + pointsSystem.ladder_points_for_match
                tB.ladder_points += -(new1_points_algo(tA.ladder_points, tB.ladder_points)) + pointsSystem.ladder_points_for_match
                tA.ladder_wins += 1
                tB.ladder_loss += 1
            elif tB_score > tA_score:
                tB.ladder_points += new1_points_algo(tB.ladder_points, tA.ladder_points) + pointsSystem.ladder_points_for_match
                tA.ladder_points += -(new1_points_algo(tB.ladder_points, tA.ladder_points)) + pointsSystem.ladder_points_for_match
                tB.ladder_wins += 1
                tA.ladder_loss += 1
        else:
            if tA_score > tB_score:
                tA.ladder_points += current_points_algo(tA.ladder_points, tB.ladder_points) + pointsSystem.ladder_points_for_match
                tB.ladder_points += -(current_points_algo(tA.ladder_points, tB.ladder_points)) + pointsSystem.ladder_points_for_match
                tA.ladder_wins += 1
                tB.ladder_loss += 1
            elif tB_score > tA_score:
                tB.ladder_points += current_points_algo(tB.ladder_points, tA.ladder_points) + pointsSystem.ladder_points_for_match
                tA.ladder_points += -(current_points_algo(tB.ladder_points, tA.ladder_points)) + pointsSystem.ladder_points_for_match
                tB.ladder_wins += 1
                tA.ladder_loss += 1
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
                                         points_deduction_multiplier= form.cleaned_data['points_deduction_multiplier'])
            new_fakematch.save()
            return redirect('/pointsdeduction')

    fakematches = FakeMatch.objects.all()
    form = FakeMatchForm()
    return render(response, 'main/fakematches.html', {'fakematches': fakematches, 'form': form})

def tournaments(response):

    if response.method == 'POST':
        form = TournamentForm(response.POST)
        if form.is_valid():
            new_tour = Tournament(name=form.cleaned_data['name'],
                                         type=form.cleaned_data['type'])
            new_tour.save()
            return redirect('/tournaments')

    tournaments = Tournament.objects.all()
    form = TournamentForm()
    return render(response, 'main/tournaments.html', {'tournaments': tournaments, 'form': form})

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

    return points_change

def ladder_ranking():
    teams = Team.objects.order_by('-ladder_points')
    rank_counter = 1
    for team in teams:
        team.ladder_rank = rank_counter
        rank_counter += 1
        team.save()

def latest_game_finder(response):
    teams = Team.objects.all()
    for team in teams:
        team.last_game = timezone.now() - timedelta(days=90)
        team.save()
        games = requests.get('https://api.projectv.gg/api/v1/frontend/participant/{}/xall_matches_to_team'.format(team.id)).json()['data']
        for game in games:
            try:
                now = timezone.now()
                date = dt.datetime.fromisoformat(game['match']['date']) # 2022-03-07T21:00:00+01:00
            except:
                now = timezone.now()
                date = timezone.now()
                
            if date < now and date > team.last_game and game['match']['status'] == 'COMPLETED':
                team.last_game = date
                team.save()
    
    return redirect('/admin')

def active_users_counter():
    teams = Team.objects.all()
    now = timezone.now()
    active_users = 0
    for team in teams:
        if team.last_game > (now - timedelta(days=100)):
            active_users += team.size
    
    return active_users
    
def tournament_results(tournament):
    matches = requests.get('https://api.projectv.gg/api/v1/frontend/tournaments/{}/xmatches'.format(tournament.id)).json()['data']
    for match in matches:
        if not match['encounters'][0]['is_bye']:
            try:
                team_A = Team.objects.get(id=match['encounters'][0]['participant']['participant_id'])
                team_A_place = match['encounters'][0]['participant']['place']
                if not Result.objects.filter(tournament=tournament, team=team_A).exists():
                    result_obj = Result(tournament=tournament, team=team_A, place=team_A_place)
                    result_obj.save()
            except Team.DoesNotExist:
                print('Team A not found')
                
        if not match['encounters'][1]['is_bye']:
            try:
                team_B = Team.objects.get(id=match['encounters'][1]['participant']['participant_id'])
                team_B_place = match['encounters'][1]['participant']['place']
                if not Result.objects.filter(tournament=tournament, team=team_B).exists():
                    result_obj = Result(tournament=tournament, team=team_B, place=team_B_place)
                    result_obj.save()
            except Team.DoesNotExist:
                print('Team B not found')
    
def dashboard(response):
    total_matches = requests.get('https://api.projectv.gg/api/v1/frontend/matches').json()['meta']['total']
    avg_matchlength = 40 #in minutes
    unplayed_matches = len(LadderMatch.objects.filter(status='COMPLETED', teamA_score=0, teamB_score=0))
    playercount_last_month = 5091 #31st of January
    total_players = requests.get('https://api.projectv.gg/api/v1/frontend/users').json()['meta']['total']
    joined_this_month = total_players - playercount_last_month
    active_users = active_users_counter()
    dropped_players = total_players - active_users
    dach_players = {
        'de': 7818,
        'ch': 350,
        'at': 587,
        'li': 1
        }
    return render(response, 'main/dashboard.html', {'hours_played': total_matches * avg_matchlength, 'unplayed_matches': unplayed_matches, 'new_players': joined_this_month, 'dropped_players': dropped_players, 'growth': joined_this_month - dropped_players, 'dach_players': dach_players})

def delete_all(response):
    matches = LadderMatch.objects.all()
    for match in matches:
        match.delete()
        
    teams = Team.objects.all()
    for team in teams:
        team.delete()
        
    results = Result.objects.all()
    for result in results:
        result.delete()
        
    return redirect('leaderboard')

def points(response):
    pointSystem = PointSystem.objects.get(id=1)
    if response.method == 'POST':
        form = PointSystemForm(response.POST)
        if form.is_valid():
            pointSystem.algo = form.cleaned_data['algo']
            pointSystem.recalculate_ladder = form.cleaned_data['recalculate_ladder']
            pointSystem.ladder_points_for_match = form.cleaned_data['ladder_points_for_match']
            pointSystem.vrc_points_for_win = form.cleaned_data['vrc_points_for_win']
            pointSystem.vrc_points_for_loss = form.cleaned_data['vrc_points_for_loss']
            pointSystem.L_pos1 = form.cleaned_data['L_pos1']
            pointSystem.L_pos2 = form.cleaned_data['L_pos2']
            pointSystem.L_pos3_4 = form.cleaned_data['L_pos3_4']
            pointSystem.L_pos5_8 = form.cleaned_data['L_pos5_8']
            pointSystem.L_pos9_16 = form.cleaned_data['L_pos9_16']
            pointSystem.L_pos17_32 = form.cleaned_data['L_pos17_32']
            pointSystem.L_pos33_64 = form.cleaned_data['L_pos33_64']
            pointSystem.L_pos65_128 = form.cleaned_data['L_pos65_128']
            pointSystem.L_pos129_256 = form.cleaned_data['L_pos129_256']
            pointSystem.M_pos1 = form.cleaned_data['M_pos1']
            pointSystem.M_pos2 = form.cleaned_data['M_pos2']
            pointSystem.M_pos3_4 = form.cleaned_data['M_pos3_4']
            pointSystem.M_pos5_8 = form.cleaned_data['M_pos5_8']
            pointSystem.M_pos9_16 = form.cleaned_data['M_pos9_16']
            pointSystem.M_pos17_32 = form.cleaned_data['M_pos17_32']
            pointSystem.M_pos33_64 = form.cleaned_data['M_pos33_64']
            pointSystem.M_pos65_128 = form.cleaned_data['M_pos65_128']
            pointSystem.M_pos129_256 = form.cleaned_data['M_pos129_256']
            pointSystem.C_pos1 = form.cleaned_data['C_pos1']
            pointSystem.C_pos2 = form.cleaned_data['C_pos2']
            pointSystem.C_pos3_4 = form.cleaned_data['C_pos3_4']
            pointSystem.C_pos5_8 = form.cleaned_data['C_pos5_8']
            pointSystem.C_pos9_16 = form.cleaned_data['C_pos9_16']
            pointSystem.C_pos17_32 = form.cleaned_data['C_pos17_32']
            pointSystem.C_pos33_64 = form.cleaned_data['C_pos33_64']
            pointSystem.C_pos65_128 = form.cleaned_data['C_pos65_128']
            pointSystem.C_pos129_256 = form.cleaned_data['C_pos129_256']
            pointSystem.F_pos1 = form.cleaned_data['F_pos1']
            pointSystem.F_pos2 = form.cleaned_data['F_pos2']
            pointSystem.F_pos3_4 = form.cleaned_data['F_pos3_4']
            pointSystem.F_pos5_8 = form.cleaned_data['F_pos5_8']
            pointSystem.F_pos9_16 = form.cleaned_data['F_pos9_16']
            pointSystem.F_pos17_32 = form.cleaned_data['F_pos17_32']
            pointSystem.F_pos33_64 = form.cleaned_data['F_pos33_64']
            pointSystem.F_pos65_128 = form.cleaned_data['F_pos65_128']
            pointSystem.F_pos129_256 = form.cleaned_data['F_pos129_256']
            pointSystem.Ladder_pos1 = form.cleaned_data['Ladder_pos1']
            pointSystem.Ladder_pos2 = form.cleaned_data['Ladder_pos2']
            pointSystem.Ladder_pos3 = form.cleaned_data['Ladder_pos3']
            pointSystem.Ladder_pos4 = form.cleaned_data['Ladder_pos4']
            pointSystem.Ladder_pos5_8 = form.cleaned_data['Ladder_pos5_8']
            pointSystem.Ladder_pos9_16 = form.cleaned_data['Ladder_pos9_16']
            pointSystem.Ladder_pos17_32 = form.cleaned_data['Ladder_pos17_32']
            pointSystem.Ladder_pos33_64 = form.cleaned_data['Ladder_pos33_64']
            pointSystem.Ladder_pos65_128 = form.cleaned_data['Ladder_pos65_128']
            pointSystem.Ladder_pos129_256 = form.cleaned_data['Ladder_pos129_256']
            
            pointSystem.save()
            return redirect('/pointsallocation')
    
    return render(response, 'main/points.html', {'pointSystem': pointSystem})

def tournament_detail(id, response):
    tour = Tournament.objects.get(id=id)
    return render(response, 'main/tour_detail.html', {'tour': tour})

def team_detail(id, response):
    team = Team.objects.get(id=id)
    return render(response, 'main/team_detail.html', {'team': team})
