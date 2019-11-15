from django.shortcuts import render
from django.contrib import sessions
import copy
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import date
import re,hashlib


# Create your views here.
def firstpage(request):
    return render(request, 'Client/first.html')

def secondpage(request):
    dynamodb=boto3.resource('dynamodb')
    table=dynamodb.Table('departments')
    response = table.scan(
                ProjectionExpression="department_name",
            )
    #print(response['Items'][0]['department_name'])

    context = response['Items']

    departments=[]
    for i in context:
        departments.append(i['department_name'])

    context={
        'departments':departments
    }

    if request.method=="POST":
        comp = request.POST['complaint']
        dynamodb=boto3.resource('dynamodb')
        table=dynamodb.Table('complaint')
        response = table.scan(
                    ProjectionExpression="complaint_id",
                )

        table.put_item(
            Item={
                'complaint_id':len(response['Items'])+1,
                'complaint':comp,

            }
            )
    return render(request, 'Client/second.html',context)

def thirdpage(request):
    return render(request, 'Client/third.html')

def track(request):
    return render(request,'Client/track.html')

def complaint(request):
        return render(request,'Client/second.html')

def client_signup(request):

    return render(request,'Client/client_signup.html')

def client_signin(request):
    #form validation
    if request.method=="POST":
        dynamodb=boto3.resource('dynamodb')
        table=dynamodb.Table('clients')
        response = table.scan()
        context = response['Items']
        username = request.POST.get('Username')
        email    = request.POST.get('email')
        password = request.POST.get('psw')
        repassword = request.POST.get('psw-repeat')
        print(username,email,password,repassword)

        #mail validation
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if(re.search(regex,email)):
            m = 1
            print('VALID EMAIL')
        else:
            m=0
        #username validation
        if(m==1):
            for con in context:
                print(con['username'],username)
                if(con['username']==username or con['email']==email):
                    print('yes')
                    return render(request,'Client/client_signup.html')
                else:
                     if(password==repassword):
                        print(password)
                        password_hashed = hashlib.sha256(password.encode())
                        password_hashed = password_hashed.hexdigest()
                        print(password_hashed)
                        table.put_item(
                            Item={
                                'client_id':len(response['Items'])+1,
                                'username':username,
                                'email':email,
                                'password':password_hashed,
                                }

                        )
                        return render(request,'Client/client_signed.html')


    return render(request,'Client/client_signup.html')


def client_login(request):
    return render(request,'Client/client_login.html')

def client_loggedin(request):
    if request.method=="POST":
        dynamodb=boto3.resource('dynamodb')
        table=dynamodb.Table('clients')
        response = table.scan()
        context = response['Items']
        email    = request.POST.get('email')
        password = request.POST.get('psw')
        password_hashed = hashlib.sha256(password.encode())
        password_hashed = password_hashed.hexdigest()
        for passw in context:
            print(passw['password'],password_hashed)
            if(passw['password'] == password_hashed):
                return render(request,'Client/client_loggedin.html')
    return render(request,'Client/client_login.html')



    
