from django.shortcuts import render
from django.http import HttpResponseRedirect
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
dynamodb = boto3.resource('dynamodb')

def formCreateMain(req):
    return render(req, "formCreation/form_main.html")

def testF(req):
    return render(req, "formCreation/form2.html")


def complaintIFrame(req):
    if 'email' in req.session and 'logged' in req.session :
        if req.method == "GET"  and req.session["logged"] == True:
            formId = req.GET["form_id"]
            table = dynamodb.Table('Complaint_forms')
            response1 = table.scan(
                FilterExpression=Attr('form_id').eq(formId)
            )

            if response1["Count"] > 0 :
                form =response1["Items"][0] 
                form0 = json.dumps(form)
                return render(req,'formCreation/iframe0.html',{'form':form0})
                
                
        if req.method == "POST" and req.session["logged"] == True :
            formId = req.POST["form_id"]
            table = dynamodb.Table('Complaint_forms')
            response1 = table.scan(
                FilterExpression=Attr('form_id').eq(formId)
            )

            if response1["Count"] > 0 :
                form =response1["Items"][0] 
                form0 = json.dumps(form)
                return render(req,'formCreation/iframe0.html',{'form':form0})
    return HttpResponseRedirect('/login/')

       
# Create your views here.



