from django.urls import path
from . import views

urlpatterns = [
    path('', views.counter),
    path('<int:number>', views.count),
    path('reset', views.count_reset),
    path('step', views.step)
]