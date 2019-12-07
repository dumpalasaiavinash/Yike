from django.shortcuts import render,redirect
import boto3
from boto3.dynamodb.conditions import Key, Attr
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib import sessions
from django.contrib import messages
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.urls import reverse


#For password hashing
import hashlib

# Create your views here.

def home(request):
    return render(request, 'home/home.html')


def home_log(request):
    # if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('pass')
    password=hashlib.sha256(password.encode())
    password=password.hexdigest()

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
                for i in range(0,len(response['Items'][0]['organizations_created'])):
                    response['Items'][0]['organizations_created'][i] = int(response['Items'][0]['organizations_created'][i])
                for i in range(0,len(response['Items'][0]['organizations_joined'])):
                    response['Items'][0]['organizations_joined'][i] = int(response['Items'][0]['organizations_joined'][i])
                request.session['username'] = response['Items'][0]['username']
                request.session['email']=response['Items'][0]['email']
                request.session['org_created']=response['Items'][0]['organizations_created']
                request.session['org_joined']=response['Items'][0]['organizations_joined']
                request.session['type'] = int(response['Items'][0]['type'])
                print(request.session['type'])
                print('abc')
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
    type = request.session['type']

    if(username!='' and email!='' and password!='' and re_password!=''):
        if(password==re_password):
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
                    'type':type,
                    }
                )
                request.session['username'] = username
                request.session['email']=email
                request.session['org_created']=[]
                request.session['org_joined']=[]
                request.session['active']=True
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
    if(type == 1):
        return render(request, "home/signup.html")
    elif(type == 2):
        # print('a')
    # print(type(int(type)))
        paypal_dict = {
            "business": 'harsha@god.com',
            "amount": 70,
            "currency-code":"USD",
            "item_name": 11,
            "invoice": 123,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": 'http://127.0.0.1:8000/signup/',
            "cancel_return": 'http://127.0.0.1:8000/',
        }

        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {"form": form}
        return render(request, "home/payments.html", context)
