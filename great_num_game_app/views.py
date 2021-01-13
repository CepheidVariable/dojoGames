from django.shortcuts import render, redirect
from random import randint
import datetime
import json


# Create your views here.
def great_num_game(request):
    if ('random' not in request.session):
        request.session['random'] = randint(1, 100)
        request.session['attempts'] = 0
        request.session['guess_result'] = "idle"
    if request.session['attempts'] == 10:
        request.session['guess_result'] = "lost"

    print(request.session['random'], request.session['attempts'])
    return render(request, 'number_game.html')


def guess(request):
    #check if valid input
    if (not request.POST['guess'].isnumeric()):
        request.session['guess_result'] = "invalid"
        return redirect('/greatnumbergame')
    elif (int(request.POST['guess']) < 1 or int(request.POST['guess']) > 100):
        request.session['guess_result'] = "invalid"
        return redirect('/greatnumbergame')
    
    # increase attempt counter
    request.session['attempts'] += 1

    #determine if guess is correct
    if int(request.POST['guess']) == request.session['random']:
        request.session['guess_result'] = "success"
        return redirect('/greatnumbergame')

    elif(int(request.POST['guess']) < (request.session['random'] + 5) and int(request.POST['guess']) > (request.session['random'] - 5)):
        request.session['guess_result'] = "near"
        return redirect('/greatnumbergame')

    elif (int(request.POST['guess']) < request.session['random']):
        request.session['guess_result'] = "low"
        return redirect('/greatnumbergame')

    elif (int(request.POST['guess']) > request.session['random']):
        request.session['guess_result'] = "high"
        return redirect('/greatnumbergame')


def reset_game(request):
    request.session['random'] = randint(1, 100)
    request.session['attempts'] = 0
    request.session['guess_result'] = "idle"
    return redirect('/greatnumbergame')


def addleader(request):
    # Serialize datetime : credit to Gabor Szabo
    def converter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()


    leader = {
        'player': request.POST['player'],
        'attempts': request.session['attempts'],
        'date': json.dumps(datetime.datetime.now(), default=converter)
    }

    if ('leaderboard' not in request.session):
        print("not leaders yet, adding first...")
        leaders = []
        request.session['leaderboard'] = leaders
        request.session['leaderboard'].append(leader)
    else:
        print("new leader added")
        request.session['leaderboard'].append(leader)
        request.session.modified = True
    
    return redirect('/greatnumbergame/leaderboard')


def leaderboard(request):
    print(request.session['leaderboard'])
    print(type(request.session['leaderboard'][0]))
    return render(request, 'leaderboard.html')