from django.urls import path
from . import views

urlpatterns = [
    path('', views.great_num_game),
    path('guess', views.guess),
    path('reset', views.reset_game),
    path('addleader', views.addleader),
    path('leaderboard', views.leaderboard),
]