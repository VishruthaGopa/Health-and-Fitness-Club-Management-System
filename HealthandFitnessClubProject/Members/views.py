from django.shortcuts import render


def profile(request):
    return render(request,'Members/profile.html')

# Create your views here.
def updateProfile(request):
    return request()