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

    if 'username' in request.session and request.session['username']:
        return redirect('/users/welcome')

    return render(request, 'index.html')

def destroy(request):
    print(f"Visits: {request.session['visits']}")
    print(f"Counter: {request.session['counter']}")
    request.session.clear()
    return redirect('/')


def users_register(request):
    if request.POST['password'] is not request.POST['confirm_password']:
        messages.error(request, "Passwords do not match.", extra_tags='register')
        return redirect('/')
    else:
        errors = User.objects.validate(request.POST)

    if errors:
        for k, v in errors.items():
            messages.error(request, v, extra_tags='register')
        return redirect('/')

    
    print("POST validated\nCleaning for user creation...")
    clean_username = User.objects.cleanup_spaces(post_pattern3=request.POST['username'])
    clean_first_name = User.objects.cleanup_spaces(post_pattern1=request.POST['first_name'])
    clean_last_name = User.objects.cleanup_spaces(post_pattern1=request.POST['last_name'])
    clean_email = User.objects.cleanup_spaces(post_pattern1=request.POST['email'])
    clean_password = User.objects.cleanup_spaces(post_pattern1=request.POST['password'])

    
    pw_hash = bcrypt.hashpw(clean_password.encode(), bcrypt.gensalt()).decode()

    User.objects.create(
        username = clean_username,
        first_name = clean_first_name.title(),
        last_name = clean_last_name.title(),
        email = clean_email,
        dob = request.POST['dob'],
        password = pw_hash
    )
    messages.info(request, "Registration successful, please login.", extra_tags='register')
    return redirect('/')


def users_login(request):
    try:
        user = User.objects.get(email=request.POST['login_email'])
    except:
        messages.error(request, "Username or password incorrect.", extra_tags='login')
        return redirect('/')

    if not bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode()):
        messages.error(request, "Username or password is invalid.", extra_tags='login')
        return redirect ('/')

    print("Successful login")
    request.session['user_id'] = user.id
    request.session['username'] = user.username

    return redirect('/users/welcome')

def users_welcome(request):
    if not 'user_id' in request.session:
        messages.error(request, "Please log in to view.", extra_tags='login')
        return redirect('/')

    return render(request, "welcome.html")

def users_logout(request):
    try:
        del request.session['user_id']
        del request.session['username']
    except:
        messages.info(request, "There was some trouble with logging you out...please try again.", extra_tags='login')
        redirect('/')

    messages.info(request, "Successfully logged out.", extra_tags='login')
    return redirect('/')