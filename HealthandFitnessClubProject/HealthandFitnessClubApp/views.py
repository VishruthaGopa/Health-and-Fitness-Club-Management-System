from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Username:", username)
        print("Password:", password)

    return render(request, 'HealthandFitnessClubApp/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Username:", username)
        print("Password:", password)

    return render(request, 'HealthandFitnessClubApp/register.html')

def updateProfile(request):
    return render(request, 'HealthandFitnessClubApp/updateProfile.html')