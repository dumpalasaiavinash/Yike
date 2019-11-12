from django.shortcuts import render

# Create your views here.
def firstpage(request):
    return render(request, 'Client/first.html')

def secondpage(request):
    return render(request, 'Client/second.html')

def thirdpage(request):
    return render(request, 'Client/third.html')