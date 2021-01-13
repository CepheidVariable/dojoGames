from django.shortcuts import render, redirect
from random import randint
import re

# Create your views here.
def great_num_game(request):
    if ('random' not in request.session):
        request.session['random'] = randint(1, 100)
        request.session['attempts'] = 0
    print(request.session['random'], request.session['attempts'])
    return render(request, 'number_game.html')

def guess(request):
    if (not request.POST['guess'].isnumeric()):
        print("Invalid guess. Try a number between 1-100.")
        return redirect('/greatnumbergame')
    
    request.session['attempts'] += 1
    # str_guess = re.sub("[^0-9]", "", request.POST['guess'])

    if int(str_guess) == request.session['random']:
        print("Correct Guess!")
        return redirect('/greatnumbergame')
    elif(int(str_guess) < (request.session['random'] + 6) and int(str_guess) > (request.session['random'] - 6)):
        print("Ooo, close! Try again.")
        return redirect('/greatnumbergame')
    else:
        print("Wrong Guess! Try again.")
        return redirect('/greatnumbergame')