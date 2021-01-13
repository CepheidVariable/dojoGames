from django.shortcuts import render, redirect
from random import randint


# Create your views here.
def great_num_game(request):
    if ('random' not in request.session):
        request.session['random'] = randint(1, 100)
        request.session['attempts'] = 0
        request.session['guess_result'] = "idle"
    print(request.session['random'], request.session['attempts'])
    return render(request, 'number_game.html')

def guess(request):
    #check if valid input
    if (not request.POST['guess'].isnumeric()):
        print("Invalid guess. Try a number between 1-100.")
        return redirect('/greatnumbergame')
    
    # increase attempt counter
    request.session['attempts'] += 1

    #determine if guess is correct
    if int(request.POST['guess']) == request.session['random']:
        print("Correct Guess!")
        
        request.session['guess_result'] = "success"
        return redirect('/greatnumbergame')
    elif(int(request.POST['guess']) < (request.session['random'] + 6) and int(request.POST['guess']) > (request.session['random'] - 6)):
        print("Ooo, close! Try again.")
        request.session['guess_result'] = "near"
        return redirect('/greatnumbergame')
    elif (int(request.POST['guess']) < request.session['random']): 
        print("Too low! Try again.")
        request.session['guess_result'] = "low"
        return redirect('/greatnumbergame')
    elif (int(request.POST['guess']) > request.session['random']): 
        print("Too high! Try again.")
        request.session['guess_result'] = "high"
        return redirect('/greatnumbergame')

def reset_game(request):
        request.session['random'] = randint(1, 100)
        request.session['attempts'] = 0
        request.session['guess_result'] = "idle"
        return redirect('/greatnumbergame')