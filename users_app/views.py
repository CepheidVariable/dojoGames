from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import User
import bcrypt

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

    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    User.objects.create(
        username = request.POST['username'],
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        dob = request.POST['dob'],
        password = pw_hash
    )
    messages.info(request, "Registration successful, please login.")
    return redirect('/')


def users_login(request):
    try:
        user = User.objects.get(email=request.POST['email'])
    except:
        messages.error(request, "Username or password incorrect.")
        return redirect('/')

    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, "Username or password is invalid.")
        return redirect ('/')

    print("Successful login")
    request.session['user_id'] = user.id
    request.session['username'] = user.username

    return redirect('/users/welcome')

def users_welcome(request):
    if not 'user_id' in request.session:
        messages.error(request, "Please log in to view.")
        return redirect('/')

    return render(request, "welcome.html")

def users_logout(request):
    try:
        del request.session['user_id']
        del request.session['username']
    except:
        messages.info(request, "There was some trouble with logging you out...please try again.")
        redirect('/')

    messages.info(request, "Successfully logged out.")
    return redirect('/')