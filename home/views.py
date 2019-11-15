from django.shortcuts import render,redirect
import boto3
from boto3.dynamodb.conditions import Key, Attr
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib import sessions



# Create your views here.

def home(request):
    return render(request, 'home/home.html')


def home_log(request):
    # if request.method == 'POST':

    email = request.POST.get('email')
    password = request.POST.get('pass')
    dynamodb = boto3.resource('dynamodb')
    if(email != '' or password!=''):
        table = dynamodb.Table('users')
        response = table.scan(
        ProjectionExpression="email,password,organizations_created,organizations_joined",
        FilterExpression=Attr('email').eq(email)
        )
        print('\n\n\n')
        print(response['Items'][0])
        print(type(response['Items'][0]['organizations_created']))
        for i in range(0,len(response['Items'][0]['organizations_created'])):
            response['Items'][0]['organizations_created'][i] = int(response['Items'][0]['organizations_created'][i])
        for i in range(0,len(response['Items'][0]['organizations_joined'])):
            response['Items'][0]['organizations_joined'][i] = int(response['Items'][0]['organizations_joined'][i])

        print('\n\n\n')
        if(len(response['Items'])>0):
            if(response['Items'][0]['password']==password):
                request.session['email']=response['Items'][0]['email']
                request.session['org_created']=response['Items'][0]['organizations_created']
                request.session['org_joined']=response['Items'][0]['organizations_joined']
                print('abc')
                return redirect('orgadmin:create')
            else:
                return redirect('home:login')
        else:
            return redirect('home:login')
    else:
        return redirect('home:login')

def home_reg(request):
    # if request.method == 'POST':
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    re_password = request.POST.get('re_pass')

    if(username!='' and email!='' and password!='' and re_password!=''):
        if(password==re_password):
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('users')
            response = table.scan(
                ProjectionExpression="email",
                FilterExpression=Attr('email').eq(email)
            )

            if(len(response['Items'])==0):
                response = table.put_item(
                   Item={
                    'username': username,
                    'email': email,
                    'password': password,
                    'organizations_created':[101],
                    'organizations_joined':[102],

                    }
                )
                return redirect('orgadmin:create')

            else:
                return redirect('home:signup')
        else:
            return redirect('home:signup')
    else:
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

   

    
