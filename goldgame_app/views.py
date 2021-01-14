from django.shortcuts import render, redirect
from random import random, randint, choices
import datetime

# Create your views here.
def goldgame(request):
    if ('gold' not in request.session):
        log_list = []
        request.session['gold'] = 0
        request.session['log'] = log_list
        request.session['gamestate'] = ""
    
    if (request.session['gamestate'] == 'lost'):
        request.session['gold'] = 0

    return render(request, 'goldgame.html')

def earngold(request):
    print(request.POST)
    if (request.POST['action'] == "mine"):
        net = randint(10, 20)
        request.session['gold'] += net
        log_data = {
            'flag': 'positive',
            'outcome': f'Earned {net} gold from the mine.',
            'date': f"({datetime.datetime.now()})"
        }
        print(log_data)
        request.session['log'].append(log_data)
        request.session.modified = True
        return redirect('/goldgame')

    elif (request.POST['action'] == "saloon"):
        net = randint(-50, 50)
        request.session['gold'] += net

        if (net > 0):
            outcome = "earned"
            flag = "positive"
        elif (net < 0):
            outcome = "lost"
            flag = "negative"
        else:
            outcome = "earned"
            flag = "none"

        log_data = {
            'flag': flag,
            'outcome': f'Entered a saloon and {outcome} {net} gold.',
            'date': f"({datetime.datetime.now()})"
        }
        print(log_data)
        request.session['log'].append(log_data)
        request.session.modified = True
        return redirect('/goldgame')

    elif (request.POST['action'] == "sheriff"):
        net = randint(10, 20)
        request.session['gold'] += net
        log_data = {
            'flag': 'positive',
            'outcome': f'Earned {net} gold from the sheriff.',
            'date': f"({datetime.datetime.now()})"
        }
        print(log_data)
        request.session['log'].append(log_data)
        request.session.modified = True
        return redirect('/goldgame')

    elif (request.POST['action'] == "bank"):
        possible_outcomes = (-1000, -500, 0, 500, 1000)
        net = choices(possible_outcomes, cum_weights=(.05, .25, .75, .95, 1.00), k=1)

        if (net[0] == 0):
            flag = "none"
            outcome = f'You robbed the bank and lost your nerve half-way through. {net[0]} gold was earned.'

        elif (net[0] == 500):
            flag = "positive"
            outcome = f'You robbed the bank and scored big! {net[0]} gold was earned.'

        elif (net[0] == -500):
            flag = "negative"
            outcome = f'You robbed the bank and were caught by the posse. {net[0]} gold for bail.'

        elif (net[0] == -1000):
            flag = "negative"
            outcome = "You robbed the bank and were shot by a pursuing posse. You died."
            request.session['gamestate'] = 'won'

        elif (net[0] == 1000):
            flag = "positive"
            outcome = "You hit the big-time! You retire into the sunset to live in infamy."
            request.session['gamestate'] = 'lost'

        request.session['gold'] += net[0]
        log_data = {
            'flag': flag,
            'outcome': outcome,
            'date': f"({datetime.datetime.now()})"
        }

        print(log_data)
        request.session['log'].append(log_data)
        request.session.modified = True
        return redirect('/goldgame')
