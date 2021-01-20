from django.urls import path
from . import views

urlpatterns = [    
    path('', views.index),
    path('users/register', views.user_create),
    path('users/login', views.user_login),
    path('destroy_session', views.destroy),
]

