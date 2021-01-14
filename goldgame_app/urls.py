from django.urls import path
from . import views

urlpatterns = [
    path('', views.goldgame),
    path('earngold', views.earngold),
    path('reset', views.reset),
    path('startgame', views.startgame)
]