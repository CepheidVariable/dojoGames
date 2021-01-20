from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import User
import bcrypt

# Create your views here.
def index(request):
    if 'visits' in request.session:
        request.session['visits'] +=1
        print(f"Visits: {request.session['visits']}")
    else :
        request.session['visits'] = 1
    
    if 'counter' in request.session:
        request.session['counter'] += request.session['step']
        print(f"Counter: {request.session['counter']}")
    else:
        request.session['counter'] = 1
        request.session['step'] = 1

    return render(request, 'index.html')

def destroy(request):
    print(f"Visits: {request.session['visits']}")
    print(f"Counter: {request.session['counter']}")
    request.session.clear()
    return redirect('/')


def users_register(request):
    errors = User.objects.validate(request.POST)

    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')

    print("Success Condition Met")

    pw_hash =bcrypt.hashpw(request.POST['password'].
    encode(), bcrypt.gensalt()).decode()

    User.objects.create(
        username = request.POST['username'],
        password = pw_hash
    )
    messages.info(request, "User created, please login.")
    return redirect('/')


def users_login(request):
    try:
        user = User.objects.get(username=request.POST['username'])
    except:
        messages.error(request, "Username or password incorrect.")
        return redirect('/')

    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        print("Successful login")
        return redirect('/')
    else:
        messages.error(request, "Username or password is invalid.")
        return redirect ('/')

