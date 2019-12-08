from django.shortcuts import render
from django.contrib import sessions
import copy
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import date
import re,hashlib
import requests

#install all of these
#pip install ndg-httpsclient
#pip install pyopenssl
#pip install pyasn1
#pip install django-dynamodb-sessions


#For sending activation function
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import datetime

#For generating token
import random
import string

check = 0
present_user = 0 
present_usermail = 0



# Create your views here.
def firstpage(request):

  

    return render(request, 'client_app/first.html',{
        
    })


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
    return render(request, 'client_app/second.html',context)

def thirdpage(request):
    return render(request, 'client_app/third.html')

def track(request):
    return render(request,'client_app/Track.html')

def complaint(request):
        return render(request,'client_app/second.html')

def client_signup(request):
    print('lsenfselnflenglsenglsengl')
    return render(request,'client_app/new_home/signup.html')

#client homepage
def client_home(request):
    return render(request,'client_app/new_home/signup.html')


def client_signin(request):
    #form validation
    if request.method=="POST":
        dynamodb=boto3.resource('dynamodb')
        table=dynamodb.Table('clients')
        response = table.scan()
        context = response['Items']
        username = request.POST.get('username')
        email    = request.POST.get('email')

        password = request.POST.get('pass')
        repassword = request.POST.get('re_pass')
        Email = email
        print(username,email,password,repassword)

        #mail validation
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

        if(re.search(regex,email)):
            m = 1
            print('VALID EMAIL')
            print(context)
        else:
            m=0
        #username validation
        if(m==1 and context != []):
            for con in context:
                print(con['username'],username)
                if(con['username']==username or con['email']==email):
                    print('yes')
                    print(con['username'],username,con['email'],email)
                    return render(request,'client_app/new_home/signup.html')
                else:
                     if(password==repassword):
                        print(password)
                        password_hashed = hashlib.sha256(password.encode())
                        password_hashed = password_hashed.hexdigest()
                        print(password_hashed)
                        letters=string.ascii_letters
                        token=''.join(random.choice(letters) for i in range(10))
                        client_id=len(response['Items'])+1
                        table.put_item(
                            Item={
                                'client_id':client_id,
                                'username':username,
                                'email':email,
                                'password':password_hashed,
                                'active':False,
                                'token':token,
                                }
                        )
                        current_site = get_current_site(request)
                        mail_subject = 'Email Confirmation'
                        message = render_to_string('client_app/acc_active_email.html', {
                            'user': username,
                            'user_email':email,
                            'domain': current_site.domain,
                            'token':token,
                            'client_id':client_id
                        })

                        to_email = email
                        email = EmailMessage(
                                    mail_subject, message, to=[to_email]
                        )
                        email.send()
                        request.session['clientname'] = username
                        client_session = request.session['clientname']
                        message = 'Hi,'+str(client_session)+' We have sent an activation link to '
                        message = message+Email
                        add = ' Click on the link to Activate your account'
                        message = message+add
                        print(message)
                        context={'client_id':client_id,'message':message}
                        return render(request,'client_app/client_signed.html',context)
        else:
            if(password==repassword):
                        print(password)
                        password_hashed = hashlib.sha256(password.encode())
                        password_hashed = password_hashed.hexdigest()
                        print(password_hashed)
                        letters=string.ascii_letters
                        token=''.join(random.choice(letters) for i in range(10))
                        client_id=len(response['Items'])+1
                        table.put_item(
                            Item={
                                'client_id':client_id,
                                'username':username,
                                'email':email,
                                'password':password_hashed,
                                'active':False,
                                'token':token,
                                }
                        )
                        current_site = get_current_site(request)
                        mail_subject = 'Email confirmation'
                        message = render_to_string('client_app/acc_active_email.html', {
                            'user': username,
                            'user_email':email,
                            'domain': current_site.domain,
                            'token':token,
                            'client_id':client_id
                        })
                        to_email = email
                        email = EmailMessage(
                                    mail_subject, message, to=[to_email]
                        )
                        email.send()
                        request.session['clientname'] = username
                        client_session = request.session['clientname']
                        print(client_session)
                        message = 'Hi,'+str(client_session)+' We have sent an activation link to'
                        message = message+Email
                        add = ' Click on link to Activate your account'
                        message = message+add
                        print(message)

                        context={'client_id':client_id,'message':message}
                        return render(request,'client_app/client_signed.html',context)

    return render(request,'client_app/new_home/signup.html')

def activate(request,token,email,username,client_id):
    dynamodb=boto3.resource('dynamodb')
    table=dynamodb.Table('clients')
    response=table.scan()

    print(token)
    print(email)
    print(username)
    print(client_id)

    for cli in response['Items']:
        if (cli['client_id']==int(client_id)) and (cli['token']==token):
            table.update_item(
                    Key={
                        'client_id':cli['client_id']
                    },
                    UpdateExpression="set active = :r",
                    ExpressionAttributeValues={
                        ':r':True
                    }
                    )
            print("______----ACcepted----_____")
            return render(request,'client_app/first.html')
        else:
            return render(request,'client_app/first.html')

def refresh(request,client_id):
    print('refresh post',client_id)
    dynamodb=boto3.resource('dynamodb')
    table=dynamodb.Table('clients')
    response=table.scan()

    for cli in response['Items']:
        if (cli['client_id']==client_id):
            if(cli['active']==True):
                print('refresh true')
                return render(request,'client_app/first.html')
            else:
                context={'client_id':client_id}
                return render(request,'client_app/client_signed.html',context)

def client_login(request):
    return render(request,'client_app/new_home/login.html')

def client_loggedin(request):
    dic = {}
    DIC = {}
    if request.method=="POST":
        dynamodb=boto3.resource('dynamodb')
        table=dynamodb.Table('clients')
        response = table.scan()
        context = response['Items']
        email = request.POST.get('email')
        password = request.POST.get('pass')
        password_hashed = hashlib.sha256(password.encode())
        password_hashed = password_hashed.hexdigest()
        for passw in context:
            print(passw['password'],password_hashed)
            if(passw['password'] == password_hashed):
                table1 =dynamodb.Table('ComplaintS')
                response = table1.scan()
                context1 = response['Items']        
                print(context1)
                
                comp_num0=[]
                comp0=[]
                comp_status0=[]
                orga_id0=[]
                empl_id0=[]
                time_stamp0=[]

                comp_num1=[]
                comp1=[]
                comp_status1=[]
                orga_id1=[]
                empl_id1=[]
                time_stamp1=[]

                name = mall(email)
                for i in context1:
                    print(i['user_email'] ,email)
                    if (i['user_email'] == email):
                        comp=''
                        if(i['complaint_status']==0):
                            comp_num0.append(i['complaint_number'])
                            comp0.append(i['Complaint'])
                            comp_status0.append(i['complaint_status'])
                            orga_id0.append(i['org_id'])
                            empl_id0.append(i['emp_id'])
                            time_stamp0.append(i['complaint_timestamp'])
                        elif(i['complaint_status']==1):
                            comp_num1.append(i['complaint_number'])
                            comp1.append(i['Complaint'])
                            comp_status1.append(i['complaint_status'])
                            orga_id1.append(i['org_id'])
                            empl_id1.append(i['emp_id'])
                            time_stamp1.append(i['complaint_timestamp'])
                    else:
                        comp = 'NO COMPLAINTS' 
                        print('NO COMPLAINTS')
                if(comp==''):
                    dic_zip0=zip(comp_num0,comp0,comp_status0,orga_id0,empl_id0,time_stamp0)
                    dic_zip1=zip(comp_num1,comp1,comp_status1,orga_id1,empl_id1,time_stamp1)
                    context={'dic0':dic_zip0,'dic1':dic_zip1,'name':name,'mail':email} 
                else:
                    dic_zip0=zip(comp_num0,comp0,comp_status0,orga_id0,empl_id0,time_stamp0)
                    dic_zip1=zip(comp_num1,comp1,comp_status1,orga_id1,empl_id1,time_stamp1)
                    context={'dic0':dic_zip0,'dic1':dic_zip1,'name':name,'mail':email,'comp':comp} 
                return render(request,'client_app/first.html',context)
            else:
                error = 'Invalid Credentials!'
                return render(request,'client_app/new_home/login.html',{'error':error})

    return render(request,'client_app/new_home/login.html')




def email_verification(request):
    return render(request,'client_app/client_signed.html')

def mall(a):
    b = 'abhishek'
    dynamodb=boto3.resource('dynamodb')
    table=dynamodb.Table('clients')
    response = table.scan()
    context = response['Items']
    for i in context:
        if(i['email'] == a):
            b = i['username']
    return b 