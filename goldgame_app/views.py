from django.shortcuts import render, redirect
from random import random, randint, choices
import datetime

# Create your views here.
def goldgame(request):
    if ('gold' not in request.session):
        log_list = []
        request.session['gold'] = 0
        request.session['log'] = log_list
    
    print(request.session['log'])
    return render(request, 'goldgame.html')

def earngold(request):
    print(request.POST)
    if (request.POST['action'] == "mine"):
        net = randint(10, 20)
        request.session['gold'] += net
        log_data = {
            'flag': True,
            'outcome': f'Earned {net} gold from the mine.',
            'date': str(datetime.datetime.now())
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
            flag = True
        else:
            outcome = "lost"
            flag = False

        log_data = {
            'flag': flag,
            'outcome': f'Entered a saloon and {outcome} {net} gold.',
            'date': str(datetime.datetime.now())
        }
        print(log_data)
        request.session['log'].append(log_data)
        request.session.modified = True
        return redirect('/goldgame')

    elif (request.POST['action'] == "sheriff"):
        net = randint(10, 20)
        request.session['gold'] += net
        log_data = {
            'flag': True,
            'outcome': f'Earned {net} gold from the sheriff.',
            'date': str(datetime.datetime.now())
        }
        print(log_data)
        request.session['log'].append(log_data)
        request.session.modified = True
        return redirect('/goldgame')

    elif (request.POST['action'] == "bank"):
        possible_outcomes = (-1000, -500, 0, 500, 1000)
        net = choices(possible_outcomes, cum_weights=(.05, .25, .75, .95, 1.00), k=1)
        print(net)
        if (net[0] == -1000):
            print("you died")
            flag = False
            outcome = "You robbed the bank and were shot by a pursuing posse. You died."
        elif (net[0] == -500):
            flag = False
            outcome = f'You robbed the bank and were caught by the posse. {net[0]} gold for bail.'
        elif (net[0] == 0):
            flag = None
            outcome = f'You robbed the bank and lost your nerve half-way through. {net[0]} gold was earned.'
        elif (net[0] == 500):
            flag = True
            outcome = f'You robbed the bank and scored big! {net[0]} gold was earned.'
        else:
            print('you won')
            flag = True
            outcome = "You hit the big-time! You retire into the sunset to live in infamy."

        request.session['gold'] += net[0]
        log_data = {
            'flag': flag,
            'outcome': outcome,
            'date': str(datetime.datetime.now())
        }
        print(log_data)
        request.session['log'].append(log_data)
        request.session.modified = True
        return redirect('/goldgame')
