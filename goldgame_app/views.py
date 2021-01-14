from django.shortcuts import render, redirect
from random import randint
import datetime

# Create your views here.
def goldgame(request):
    if ('gold' not in request.session):
        log_list = []
        request.session['gold'] = 0
        request.session['log'] = log_list
    return render(request, 'goldgame.html')

def earngold(request):
    print(request.POST)
    if (request.POST['action'] == "mine"):
        outcome = randint(10, 20)
        request.session['gold'] += outcome
        log_data = {
            'flag': True,
            'outcome': f'Earned {outcome} gold from the {request.POST["action"]}.',
            'date': str(datetime.datetime.now())
        }
        print(log_data)
        return redirect('/goldgame')
    elif (request.POST['action'] == "saloon"):
        request.session['gold'] += randint(-50, 50)
        return redirect('/goldgame')
    elif (request.POST['action'] == "sheriff"):
        request.session['gold'] += randint(5, 10)
        return redirect('/goldgame')
    elif (request.POST['action'] == "bank"):
        request.session['gold'] += randint(10, 20)
        return redirect('/goldgame')
