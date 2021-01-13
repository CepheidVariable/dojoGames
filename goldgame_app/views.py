from django.shortcuts import render

# Create your views here.
def goldgame(request):
    return render(request, 'goldgame.html')