from django.shortcuts import render, redirect
from random import random, randint, choices
import datetime

# Create your views here.
def goldgame(request):
    if ('gold' not in request.session):
        return render(request, 'startgame.html')

    return render(request, 'goldgame.html')


def earngold(request):
    print(request.POST)
    
    if (request.POST['action'] == "mine"):
        net = randint(20, 40)
        log_data = {
            'flag': 'positive',
            'outcome': f'Earned {net} gold from the mine.',
            'date': f"({datetime.datetime.now()})"
        }
        # print(log_data)
        # request.session['log'].append(log_data)
        # request.session.modified = True
        # return redirect('/goldgame')

    elif (request.POST['action'] == "saloon"):
        net = randint(-100, 150)

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
        # print(log_data)
        # request.session['log'].append(log_data)
        # request.session.modified = True
        # return redirect('/goldgame')

    elif (request.POST['action'] == "sheriff"):
        net = randint(0, 100)
        log_data = {
            'flag': 'positive',
            'outcome': f'Earned {net} gold from the sheriff.',
            'date': f"({datetime.datetime.now()})"
        }
        # print(log_data)
        # request.session['log'].append(log_data)
        # request.session.modified = True
        # return redirect('/goldgame')

    elif (request.POST['action'] == "bank"):
        possible_outcomes = (-1000, -500, 0, 500, 1000)
        temp = choices(possible_outcomes, cum_weights=(.05, .25, .75, .95, 1.00), k=1)
        net = temp[0]

        if (net == 0):
            flag = "none"
            outcome = f'You robbed the bank and lost your nerve half-way through. {net} gold was earned.'

        elif (net == 500):
            flag = "positive"
            outcome = f'You robbed the bank and scored big! {net} gold was earned.'

        elif (net == -500):
            flag = "negative"
            outcome = f'You robbed the bank and were caught by the posse. {net} gold for bail.'

        elif (net == -1000):
            flag = "negative"
            outcome = "You robbed the bank and were shot by a pursuing posse. You died."
            request.session['gamestate'] = 'lost'

        elif (net == 1000):
            flag = "positive"
            outcome = "You hit the big-time! You retire into the sunset to live in infamy."
            request.session['gamestate'] = 'won'

        log_data = {
            'flag': flag,
            'outcome': outcome,
            'date': f"({datetime.datetime.now()})"
        }
        

    print(log_data)
    request.session['gold'] += net
    request.session['turn'] += 1
    request.session['log'].append(log_data)
    request.session.modified = True

    if (request.session['turn_limit'] <= request.session['turn']):
        request.session['gamestate'] = "lost"
    elif (request.session['gold'] >= request.session['gold_goal']):
        request.session['gamestate'] = "won"

    return redirect('/goldgame')


def reset(request):
    del request.session['gold']
    del request.session['log']
    del request.session['gamestate']
    del request.session['turn']
    del request.session['turn_limit']
    del request.session['gold_goal']

    return render(request, 'startgame.html')


def startgame(request):
    if ('gold' not in request.session):
        log_list = []
        request.session['gold'] = 0
        request.session['log'] = log_list
        request.session['gamestate'] = ""
        request.session['turn'] = 0

    if (request.POST['turns'].isnumeric()):
        str_turns = request.POST['turns'].strip()
        str_turns = str_turns.replace(" ", "")
        request.session['turn_limit'] = int(str_turns)
    else:
        request.session['turn_limit'] = str(request.POST['default_turns'])

    if (request.POST['goal'].isnumeric()):
        str_goal = request.POST['goal'].strip()
        str_goal = str_goal.replace(" ", "")
        request.session['gold_goal'] = int(str_goal)
    else:
        request.session['gold_goal'] = str(request.POST['default_gold'])

    return redirect('/goldgame')