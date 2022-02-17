from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update_database', views.update_database, name='update_database'),
    path('run_calculation', views.run_calculation, name='run_calculation'),
    path('reset_ladder_points', views.reset_ladder_points, name= 'reset_ladder_points'),
    path('leaderboard', views.ranking, name='leaderboard'),
    path('pointsdeduction', views.points_deduction, name='fakematches')
]