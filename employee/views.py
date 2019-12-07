from django.shortcuts import render,redirect
from django.contrib import sessions
import copy
import boto3
from boto3.dynamodb.conditions import Key, Attr
import random
from urllib import parse
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import requires_csrf_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



from django.contrib import messages

import datetime

# Create your views here.


    

def juniors(request):
    return render(request, 'employee/juniors.html')

def dashboard(request,j):
    email=request.session['email']
    print(email)

    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('employees')

    response_complaint = dynamoTable.scan(
        ProjectionExpression="emp_id",
        FilterExpression=Attr('user_email').eq(email)
    )
    employee_id=response_complaint['Items'][0]['emp_id']
    
    print(response_complaint)

    # if(len(response_complaint['Items'])==0):
    #     data={'complaint': " ",'count':len(new_complaint)}
    #     return render(request, 'employee/index.html',data)
  

    #print(response_complaint)
        
        
    # getting complaints from db
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('ComplaintS')
    response_disp_complaint = dynamoTable.scan(
        ProjectionExpression="Complaint,complaint_number,org_id",
        FilterExpression = Attr('emp_id').eq(employee_id),
    )
    # print(response_disp_complaint) 
    # print(len(response_disp_complaint['Items']))
    complaints=[]
    complaint_id=[]
    org_id=[]
    for i in range(0,len(response_disp_complaint['Items'])):
        complaints.append(response_disp_complaint['Items'][i]['Complaint'])
        complaint_id.append(response_disp_complaint['Items'][i]['complaint_number'])
        org_id.append(response_disp_complaint['Items'][i]['org_id'])
    print(complaints)
    print(org_id)
    print(complaint_id)
    ids=str(org_id)
    list1=[]
    list1.append(ids.split("'"))
    list2=[]
    for i in range(0,len(list1[0])):
        if i%2 != 0:
            list2.append(int(list1[0][i]))
    print(list2)
    new_complaint=[]
    new_complaint_id=[]
    for i in range(0,len(response_disp_complaint['Items'])):
        if list2[i]==j:
            new_complaint.append(complaints[i])
            new_complaint_id.append(complaint_id[i])
    print("@@@@@@@@@@@@@@")
    print(new_complaint_id)
    print(new_complaint)
    print(len(new_complaint))
    
    data={'complaint': new_complaint,'count':len(new_complaint)}

    return render(request, 'employee/index.html',data)

