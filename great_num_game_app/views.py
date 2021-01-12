from django.shortcuts import render, redirect

# Create your views here.
def great_num_game(request):
    return render(request, 'number_game.html')