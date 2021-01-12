from django.shortcuts import render, redirect
from random import randint

# Create your views here.
def great_num_game(request):
    if ('random' not in request.session):
        request.session['random'] = randint(1, 100)
        request.session['guess'] = ""
    print(request.session['random'], request.session['guess'])
    return render(request, 'number_game.html')

def guess(request):
    str_guess = request.POST['num_guess'].strip()
    str_guess = str_guess.replace(" ", "")
    if int(str_guess) == request.session['random']:
        print("Correct Guess!")
        return redirect('/greatnumbergame')
    else:
        print("Wrong Guess!")
        return redirect('/greatnumbergame')