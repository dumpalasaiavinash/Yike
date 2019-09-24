from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def login(request):
    return render(request, 'home/login.html')
