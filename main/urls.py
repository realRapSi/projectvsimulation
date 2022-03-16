from django.urls import path
from . import views

urlpatterns = [
    path('update_database', views.update_database, name='update_database'),
    path('run_calculation', views.run_calculation, name='run_calculation'),
    path('reset_ladder_points', views.reset_ladder_points, name= 'reset_ladder_points'),
    path('', views.ranking, name='leaderboard'),
    path('pointsdeduction', views.points_deduction, name='fakematches'),
    path('latestgamefinder', views.latest_game_finder, name='latest_game_finder'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('delete_all', views.delete_all, name= 'delete_all'),
    path('pointsallocation', views.points, name= 'points'),
    path('tournaments', views.tournaments, name= 'tournaments'),
    path('tournaments/<str:id>', views.tournament_detail, name= 'tournament_detail'),
    path('teams/<str:id>', views.team_detail, name= 'team_detail'),
]