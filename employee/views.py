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
from datetime import datetime


from django.contrib import messages

import datetime

# Create your views here.


def juniors(request):
    if(request.session['type']==1):
        context = {"name":request.session['username'],"j":request.session['j']}
        return render(request, 'employee/disabled_juniors.html',context)
    else:
       
        return render(request, 'employee/juniors.html')


def dashboard(request,j):
    email=request.session['email']
    print(email)
    request.session['Employee_org']=j

    request.session['j'] = j
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('employees')

    response_complaint = dynamoTable.scan(
        ProjectionExpression="emp_id",
        FilterExpression=Attr('user_email').eq(email)
    )
    print(response_complaint['Items'])
    if (len(response_complaint['Items'])==0):
        return render(request, 'employee/index.html')

    else:

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
            ProjectionExpression="Complaint,complaint_number,org_id,complaint_status,complaint_timestamp",
            FilterExpression = Attr('emp_id').eq(employee_id) & Attr('complaint_status').eq(0),
        )
        #print(response_disp_complaint) 
        # print(len(response_disp_complaint['Items']))

        complaints=[]
        complaint_id=[]
        org_id=[]
        Status=[]
        date=[]
        for i in range(0,len(response_disp_complaint['Items'])):
            complaints.append(response_disp_complaint['Items'][i]['Complaint'])
            complaint_id.append(response_disp_complaint['Items'][i]['complaint_number'])
            org_id.append(response_disp_complaint['Items'][i]['org_id'])
            Status.append(response_disp_complaint['Items'][i]['complaint_status'])
            date.append(response_disp_complaint['Items'][i]['complaint_timestamp'])
        print(complaints)
        print(Status)
        print(org_id)
        print(complaint_id)
        print(date)
        datefinal=[]
        for i in date:
            datefinal.append(i[0:8])
        print(datefinal)
        print(datetime.date.today())
        currentdate=datetime.date.today()
        a=str(currentdate)
        print("a:"+a)
        currentdate_final=a[0:4]+a[5:7]+a[8:10]
        print(currentdate_final)
        count_date=0
        for i in datefinal:
            if (int(currentdate_final)-int(i)>1):
                print("**********")
                print(int(currentdate_final),int(i))
                print("!!!!!!!!!!!!")
                count_date=count_date+1
        print(count_date)
        b=[]
        for i in datefinal:
            b.append(i[0:4]+"-"+i[4:6]+"-"+i[6:8])
        print(b)
        
        dynamoDB=boto3.resource('dynamodb')
        dynamoTable=dynamoDB.Table('ComplaintS')
        response_complaint_status = dynamoTable.scan(
            ProjectionExpression="complaint_status",
            FilterExpression = Attr('emp_id').eq(employee_id) & Attr('complaint_status').eq(1),
        )
        
        status_processed=len(response_complaint_status['Items'])
        # Status_processed.append(response_complaint_status['Items'][i]['complaint_status'])
        # status1=[]
        # sta=str(Status_processed)
        # status1.append(sta.split("'"))
        # status2=[]
        # for i in range(0,len(status1[0])):
        #     if i%2 != 0:
        #         status2.append(int(status1[0][i]))
        # print(status2)
        # count_dealed=0  
        # for i in status2:
        #     if i==1:
        #         count_dealed=count_dealed+1
        count_dealed=status_processed
        ids=str(org_id)
        list1=[]
        list1.append(ids.split("'"))
        list2=[]
        for i in range(0,len(list1[0])):
            if i%2 != 0:
                list2.append(int(list1[0][i]))
        print(list2)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
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
        notification=[]
        if len(new_complaint)==0:
            notification.append("Well done. No complaints left for today. ")
        if (count_date==0):
            notification.append("High Priprity Complaints are completed, do the rest and make your organization proud")
        print(notification)

        print(j)
        print("@@@@@@@@@@@@@@@@@@@@@@@@")
        dynamoDB=boto3.resource('dynamodb')
        dynamoTable=dynamoDB.Table('ComplaintS')
        response_juiors_stats = dynamoTable.scan(
            ProjectionExpression="complaint_number",
            FilterExpression = Attr('org_id').eq(str(j))
        )
        print(response_juiors_stats)
        total_complaints=len(response_juiors_stats['Items'])
        print(total_complaints)

        dynamoDB=boto3.resource('dynamodb')
        dynamoTable=dynamoDB.Table('ComplaintS')
        response_juiors_left = dynamoTable.scan(
            ProjectionExpression="complaint_number",
            FilterExpression = Attr('org_id').eq(str(j)) & Attr('complaint_status').eq(0) 
        )
        print(response_juiors_left)
        total_left=len(response_juiors_left['Items'])
        print(total_left)

        dynamoDB=boto3.resource('dynamodb')
        dynamoTable=dynamoDB.Table('ComplaintS')
        response_juiors_done = dynamoTable.scan(
            ProjectionExpression="complaint_number",
            FilterExpression = Attr('org_id').eq(str(j)) & Attr('complaint_status').eq(1) 
        )
        print(response_juiors_done)
        total_done=len(response_juiors_done['Items'])
        print(total_done)










        data={'complaint':zip(new_complaint,b,complaint_id),'count':len(new_complaint),'count_dealed':count_dealed,'count_date':count_date,'notification':notification,'org_id':j,'total_done':total_done,'total_left':total_left,'total_complaints':total_complaints }

        return render(request, 'employee/index.html',data)



def validate(request,complaint_id,org_id):
    email=request.session['email']
    print(email)

    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('employees')

    response_complaint = dynamoTable.scan(
        ProjectionExpression="emp_id",
        FilterExpression=Attr('user_email').eq(email)
    )
    employee_id=response_complaint['Items'][0]['emp_id']

    dynamoDB=boto3.resource('dynamodb')
    table=dynamoDB.Table('ComplaintS')
    response = table.update_item(
        Key={
            'complaint_number':complaint_id
        },
        UpdateExpression="set complaint_status = :r",
        ExpressionAttributeValues={
            ':r': 1,
        },
        ReturnValues="UPDATED_NEW"
        )

    url="../../"+str(org_id)
    return redirect(url)
