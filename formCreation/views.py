from django.shortcuts import render

def formCreateMain(req):
    return render(req, "formCreation/form_main.html")

def testF(req):
    return render(req, "formCreation/form2.html")
# Create your views here.
