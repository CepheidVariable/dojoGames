from django.urls import path
from . import views

urlpatterns = [    
    path('', views.index),
    path('user/create', views.user_create),
    path('user/login', views.user_login),
    path('destroy_session', views.destroy),
]

