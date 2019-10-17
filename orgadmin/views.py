from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/index.html')

def create(request):
    return render(request, 'orgadmin/create.html')
def createform(request):
    return render(request,'orgadmin/createform.html')