from django.shortcuts import render, redirect

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