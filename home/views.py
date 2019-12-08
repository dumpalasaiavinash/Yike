from django.shortcuts import render,redirect
import boto3
from boto3.dynamodb.conditions import Key, Attr
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib import sessions
from django.contrib import messages
from datetime import date
import datetime
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.urls import reverse

#For password hashing
import hashlib

# Create your views here.

def home(request):
    print(request.session.keys())
    x = []
    for key in request.session.keys():
        x.append(key)
        # print(key)
    for i in x:
        del request.session[i]
    print(request.session.keys())

    return render(request, 'home/home.html')


def home_log(request):
    # if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('pass')
    password=hashlib.sha256(password.encode())
    password=password.hexdigest()
    type=1
    if('type' in request.session.keys()):
        type = request.session['type']
    else:
        request.session['type']=1

    dynamodb = boto3.resource('dynamodb')
    if(email != '' or password!=''):
        table = dynamodb.Table('users')
        response = table.scan(FilterExpression=Attr('email').eq(email))
        print(response)
        # response = table.scan(
        # ProjectionExpression="email,password,organizations_created,organizations_joined,username",
        # FilterExpression=Attr('email').eq(email)
        # )
        print('\n\n\n')
        print(response['Items'])
        # print(response['Items'][0])

        print('\n\n\n')
        if(len(response['Items'])>0):
            if(response['Items'][0]['password']==password):

                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('payments')

                inv_response = table.scan(
                    ProjectionExpression="dat",
                    FilterExpression=Attr('email').eq(email),
                )

                now = datetime.datetime.now()
                l_date = datetime.date(now.year, now.month, now.day)
                f_date = datetime.date(now.year, now.month, now.day)
                print(inv_response['Items'])
                if((inv_response['Items']!=[]) and ('dat' in inv_response['Items'][0])):
                    f_date = inv_response['Items'][0]['dat']
                delta = l_date - f_date
                for i in range(0,len(response['Items'][0]['organizations_created'])):
                    response['Items'][0]['organizations_created'][i] = int(response['Items'][0]['organizations_created'][i])
                for i in range(0,len(response['Items'][0]['organizations_joined'])):
                    response['Items'][0]['organizations_joined'][i] = int(response['Items'][0]['organizations_joined'][i])
                request.session['username'] = response['Items'][0]['username']
                request.session['email']=response['Items'][0]['email']
                request.session['org_created']=response['Items'][0]['organizations_created']
                request.session['org_joined']=response['Items'][0]['organizations_joined']
                # if(request.session['type'] != int(response['Items'][0]['type'])):
                    # request.session['type'] = int(response['Items'][0]['type'])
                if(int(response['Items'][0]['typ']) == 2):
                    request.session['type'] = 2
                print(request.session['type'])
                # print('abc')
                if(delta.days > 30):
                    request.session['type'] = 1

                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('payments')

                inv_response = table.scan(
                    ProjectionExpression="invoice",
                )
                invoice=1
                if(len(inv_response['Items'])==0):
                    invoice=1
                else:
                    for i in inv_response['Items']:
                        if(invoice<int(i['invoice'])):
                            invoice = int(i['invoice'])
                if(type == 2):
                    print('a')
                    paypal_dict = {
                        "business": 'harsha@god.com',
                        "amount": 70,
                        "currency-code":"USD",
                        "item_name": email,
                        "invoice": invoice+1000,
                        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                        "return": 'http://127.0.0.1:8000/orgadmin/pre_create',
                        "cancel_return": 'http://127.0.0.1:8000/',
                    }
                    form = PayPalPaymentsForm(initial=paypal_dict)
                    context = {"form": form,"name":request.session['username']}
                    return render(request, "home/payments.html", context)


                return redirect('orgadmin:create')
            else:
                messages.success(request, 'Failed to login as the password does not match.')
                return redirect('home:login')
        else:
            messages.success(request, 'Failed to login as the email ID is not registered.')
            return redirect('home:login')
    else:
        messages.success(request, 'Failed to login as the email or password is provided empty')
        return redirect('home:login')

def home_reg(request):
    # if request.method == 'POST':
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    re_password = request.POST.get('re_pass')
    type=1
    if('type' in request.session.keys()):
        type = request.session['type']
        print(type)
    else:
        request.session['type']=1

    if(username!='' and email!='' and password!='' and re_password!=''):
        if(password==re_password):


            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('payments')

            inv_response = table.scan(
                ProjectionExpression="invoice",
            )
            invoice=1
            if(len(inv_response['Items'])==0):
                invoice=1
            else:
                for i in inv_response['Items']:
                    if(invoice<int(i['invoice'])):
                        invoice = int(i['invoice'])

            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('users')

            response = table.scan(
                ProjectionExpression="email",
                FilterExpression=Attr('email').eq(email)
            )
            password=hashlib.sha256(password.encode())
            password=password.hexdigest()

            if(len(response['Items'])==0):
                response = table.put_item(
                   Item={
                    'username': username,
                    'email': email,
                    'password': password,
                    'organizations_created':[],
                    'organizations_joined':[],
                    'active':True,
                    'typ':type,
                    }
                )
                request.session['username'] = username
                request.session['email']=email
                request.session['org_created']=[]
                request.session['org_joined']=[]
                request.session['active']=True
                if(type == 2):
                    paypal_dict = {
                        "business": 'harsha@god.com',
                        "amount": 70,
                        "currency-code":"USD",
                        "item_name": email,
                        "invoice": invoice+1000,
                        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                        "return": 'http://127.0.0.1:8000/orgadmin/pre_create',
                        "cancel_return": 'http://127.0.0.1:8000/',
                    }

                # Create the instance.
                    form = PayPalPaymentsForm(initial=paypal_dict)
                    context = {"form": form}
                    return render(request, "home/payments.html", context)

                return redirect('orgadmin:create')

            else:
                messages.success(request, 'The email ID is already registerd.')
                return redirect('home:signup')
        else:
            messages.success(request, 'Failed to register as the password and retype password do not match.')
            return redirect('home:signup')
    else:
        messages.success(request, 'Failed to register as some fields are not provided.')
        return redirect('home:signup')


def login(request):
    return render(request, 'home/login.html')

def signup(request):
    return render(request, 'home/signup.html')


class user_logged_in(APIView):
    def post(self,request):
        print(request.data)
        for each in request.data:
            email = each['email']

        request.session['email'] = email
        print(email)
        return Response()

    def get(self, request):
        email=request.session['email']
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('users')
        response = table.scan(
        ProjectionExpression="email,username",
        FilterExpression=Attr('email').eq(email)
        )
        data = []
        print(response['Items'][0]['username'])
        var = {
            'username': response['Items'][0]['username']
        }
        data.append(var)
        return Response(data)




def payments(request,type):
    # What you want the button to do.
    print(type)
    request.session['type'] = type

    # dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table('payments')
    # response = table.scan()
    # if(len(response['Items'])==0):
    #     invoice = 0
    # else:
    #     invoice = 0
    #     if(response['Items'][]):
    if(type == 1):
        return render(request, "home/login.html")
    elif(type == 2):
        # print('a')
    # print(type(int(type)))
        return render(request, "home/login.html")
