from django.urls import path
from . import views

urlpatterns = [    
    path('', views.index),
    path('users/register', views.users_register),
    path('users/login', views.users_login),
    path('destroy_session', views.destroy),
]

