from django.shortcuts import render
from django.http import HttpResponseRedirect
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from django import forms
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

def formCreateMain(req):
    if "email" in req.session  and  "org_id" in req.session :
        return render(req, "formCreation/form_main.html",{"org_id":req.session["org_id"]})
    return HttpResponseRedirect('/login/')

def testF(req):
    return render(req, "formCreation/form2.html")


def complaintIFrame(req):
    if 'email' in req.session  :
        if req.method == "GET" :
            formId = req.GET["form_id"]
            table = dynamodb.Table('Complaint_forms')
            response1 = table.scan(
                FilterExpression=Attr('form_id').eq(formId)
            )

            if response1["Count"] > 0 :
                form =response1["Items"][0]
                print(form)
                form0 = json.dumps(form)
                return render(req,'formCreation/iframe0.html',{'form':form0})


        if req.method == "POST":
            formId = req.POST["form_id"]
            foRm=ComplaintForm(req.POST)

            table = dynamodb.Table('Complaint_forms')
            response1 = table.scan(
                FilterExpression=Attr('form_id').eq(formId)
            )

            if response1["Count"] > 0 :
                form =response1["Items"][0]
                if foRm.is_valid():
                    Complaint00 = {}
                    print(req.POST)
                    for field in form :

                        print(field)
                        if field not in ["form_id" , "org_id" ] :
                            data00 = json.loads(form[field])
                            typE = data00["type"]
                            if typE in ["textfield","datepicker","textarea","radiogroup"] :
                                #if req.POST[field] == "" :
                                    #return render(req,'formCreation/iframe0.html',{'form':form0,"msg":"error"})
                                Complaint00[data00["label"]] = req.POST[field]

                            elif typE == "mobile" :
                                Complaint00[data00["label"]] = req.POST[field+"_0"]+req.POST[field+"_1"]

                            elif typE == "image_Upload" or typE == "file_Upload" :
                                fname = req.session["email"] + datetime.now().strftime("%Y%m%d%H%M")
                                Complaint00[data00["label"]] = fname
                                handle_uploaded_file(req.FILES[field],fname)
                            elif typE == "checkgroup" :
                                print(data00)
                                datum00  = {}
                                i = 0
                                lim = data00['nR']
                                while(i<lim):
                                    datum00[data00['checks'][str(i)]['label']] = req.POST[field+"_"+str(i)]
                                    print("0")
                                    i += 1
                                Complaint00[data00['label']] = json.dumps(datum00)



                        elif field == "form_id":
                            Complaint00["form_id"]  =   req.POST[field]

                        elif field == "org_id" :
                            Complaint00["org_id"] = req.POST[field]

                    Complaint00["user_email"] = req.session["email"]
                    Complaint00["complaint_status"] = 0
                    Complaint00["complaint_timestamp"] = datetime.now().strftime("%Y%m%d%H%M%S")


                    table = dynamodb.Table("ComplaintS")
                    response1 = table.scan()
                    u_id = len(response1['Items'])+1
                    Complaint00["complaint_number"] = "Complaint" + str(u_id)
                    table.put_item(
                        Item= Complaint00
                    )
                    return HttpResponseRedirect("/")


                form0 = json.dumps(form)

                print(req.POST)
                return render(req,'formCreation/iframe0.html',{'form':form0})

    return HttpResponseRedirect('/login/')



# Create your views here.



def handle_uploaded_file(f , filename):
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class ComplaintForm(forms.Form):
    print("hello")
