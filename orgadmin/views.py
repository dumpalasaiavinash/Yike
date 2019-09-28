from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def create(request):
    return render(request, 'orgadmin/create.html')
