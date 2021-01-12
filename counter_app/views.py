from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def counter(request):
    if (not 'counter' in request.session):
        request.session['counter'] = 0
    return render(request, 'counter.html')

def count(request,number):
    for x in range(number):
        request.session['counter'] += request.session['step']

    return redirect('/counter')

def count_reset(request):
    del request.session['counter']
    return redirect('/counter')

def step(request):
    print(request.POST)
    if (request.POST['new_step'] == ""):
        request.session['step'] = int(request.POST['default_step'])
        print("No new step. Used default value.")
        return redirect('/counter')
    else:
        str_new = request.POST['new_step'].strip()
        str_new = str_new.replace(" ", "")
        request.session['step'] = int(str_new)
    return redirect('/counter')