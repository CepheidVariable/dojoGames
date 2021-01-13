from django.shortcuts import render

# Create your views here.
def goldgame(request):
    if ('gold' not in request.session):
        request.session['gold'] = 0
    return render(request, 'goldgame.html')