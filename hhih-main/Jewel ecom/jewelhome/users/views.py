from django.shortcuts import render
from datetime import datetime
# Create your views here.

def Home(request):

    return render(request, 'users/home.html')