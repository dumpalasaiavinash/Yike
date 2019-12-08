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
        present=0 #User already present in organisation
        org_id = request.session['Employee_org']
        # request.session['org_id']=org_id
        dynamodb=boto3.resource('dynamodb')
        table=dynamodb.Table('employees')
        departments_table=dynamodb.Table('departments')
        org_table=dynamodb.Table('organization')

        org_response=org_table.scan()
        dep_response=departments_table.scan()
        response2=table.scan()
        #Getting departments from departments table
        dep=[]

        no_of_departments=0
        no_of_employees=0
        no_of_complaints=0

        #Getting Organisation Name
        for org in org_response['Items']:
            if(org['org_id']==org_id):
                organisation_name=org['organization_name']

        # Checking for no_of_complaintsand no_of_employees
        for emp_dic in response2['Items']:
            if(emp_dic['org_id']==org_id) and (emp_dic['active']==True):
                no_of_employees=no_of_employees+1
                no_of_complaints=no_of_complaints+int(emp_dic['no_complaints'])

        #Used for storing employeees in list and counting no of departments in organisation
        for de in dep_response['Items']:
            if(de['organization_id']==org_id):
                no_of_departments=no_of_departments+1
                dep.append(de['department_name'])


        for dic in response2['Items']:
            if dic['active']==True and dic['org_id']==int(org_id):
                if dic['department'] not in dep:
                    print("Hi",dic['department'],dic['emp_id'],dic['emp_name'])
                    table.delete_item(
                        Key={
                            'emp_id': dic['emp_id']
                        },
                    )
        table=dynamodb.Table('employees')
        response2=table.scan()

        name=[]
        department=[]
        hierarchy=[]
        no_complaints=[]
        emp_id=[]

        for dic in response2['Items']:
            if dic['active']==True and dic['org_id']==int(org_id):
                name.append(dic['emp_name'])
                department.append(dic['department'])
                hierarchy.append(dic['hierarchy'])
                no_complaints.append(dic['no_complaints'])
                emp_id.append(dic['emp_id'])


        info_list=zip(name,department,hierarchy,no_complaints,emp_id)

        context={
            'info_list':info_list,
            'org_id':org_id,
            'dep':dep,
            'present':present,
            'no_of_departments':no_of_departments,
            'no_of_employees':no_of_employees,
            'no_of_complaints':no_of_complaints,
            'organisation_name':organisation_name
        }

        if request.method=='POST':
            name=request.POST.get('emp_name')
            department=request.POST.get('department')
            hierarchy=request.POST.get('hierarchy')
            no_comp=request.POST.get('no_complaints')
            email=request.POST.get('emp_email')

            dynamodb=boto3.resource('dynamodb')
            table=dynamodb.Table('employees')
            email_present_table=dynamodb.Table('users')

            #Checking if user is already registered user or not
            email_present=email_present_table.scan(
                ProjectionExpression="email",
            )

            check=0
            for em in email_present['Items']:
                if(em['email']==email):
                    check=1
            #End of user checking

            #Incrementing the primary key
            response = table.scan(
                        ProjectionExpression="emp_id",
                    )

            #Checking if person with entered email already present in organisation or not
            for dic in response2['Items']:
                if(dic['user_email']==email) and (dic['org_id']==org_id):
                    present=1
                    context['present']=present
                    return render(request, 'employee/juniors.html',context)

            emp_id=len(response['Items'])+1

            #Randomly generating password
            letters=string.ascii_letters
            password_gen=''.join(random.choice(letters) for i in range(8))
            token=''.join(random.choice(letters) for i in range(10))

            #Checking if the user admin entered is regestered user or a new user
            #Below if new user is added
            if (check==0):

                table.put_item(
                Item={
                    'org_id':org_id,
                    'emp_id':len(response['Items'])+1,
                    'emp_name':name,
                    'user_email':email,
                    'department':department,
                    'hierarchy':hierarchy,
                    'no_complaints':no_comp,
                    'active':False,
                    'token':token
                 }
                )

                current_site = get_current_site(request)
                mail_subject = 'Click the link to join the organisation.'
                message = render_to_string('dashboard/acc_active_email.html', {
                    'user': name,
                    'user_id':emp_id,
                    'user_email':email,
                    'password':password_gen,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(emp_id)),
                    'token':token,
                    'org_id':org_id
                })
                to_email = email
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()

                return render(request, 'employee/juniors.html',context)



            #If user already registered is in added to organisation
            elif(check==1):
                table.put_item(
                Item={
                    'org_id':org_id,
                    'emp_id':len(response['Items'])+1,
                    'emp_name':name,
                    'user_email':email,
                    'department':department,
                    'hierarchy':hierarchy,
                    'no_complaints':no_comp,
                    'active':True,
                    'token':token
                 }
                )

                current_site = get_current_site(request)
                mail_subject = 'Joined organisation login with your old credentials.'
                message = render_to_string('dashboard/old_credentials_email.html', {
                    'user': name,
                    'user_id':emp_id,
                    'user_email':email,
                    'password':password_gen,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(emp_id)),
                    'token':token,
                    'org_id':org_id
                })
                to_email = email
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()

                #Database call for getting updated table(After registered user is added)
                table2=dynamodb.Table('employees')
                user_table=dynamodb.Table('users')
                dept_table=dynamodb.Table('departments')
                org_table=dynamodb.Table('organization')

                org_response=org_table.scan()
                dept_response=dept_table.scan()
                user_response=user_table.scan()
                response3=table2.scan()

                for user in user_response['Items']:
                    if(user['email']==email):
                        org_joined=user['organizations_joined']
                        org_joined.append(org_id)

                        user_table.update_item(
                            Key={
                                'user_email':dic['user_email']
                            },
                        )



                dep=[]

                no_of_departments=0
                no_of_employees=0
                no_of_complaints=0

                #Getting Organisation Name
                for org in org_response['Items']:
                    if(org['org_id']==org_id):
                        organisation_name=org['organization_name']

                #Used for getting department list and no of departments
                for de in dept_response['Items']:
                    if(de['organization_id']==org_id):
                        no_of_departments=no_of_departments+1
                        dep.append(de['department_name'])

                # Checking for no_of_complaintsand no_of_employees
                for emp_dic in response3['Items']:
                    if(emp_dic['org_id']==org_id) and (emp_dic['active']==True):
                        no_of_employees=no_of_employees+1
                        no_of_complaints=no_of_complaints+int(emp_dic['no_complaints'])

                for dic in response3['Items']:
                    if dic['active']==True and dic['org_id']==int(org_id):
                        if dic['department'] not in dep:
                            table2.delete_item(
                                Key={
                                    'emp_id': dic['emp_id']
                                },
                            )


                name=[]
                department=[]
                hierarchy=[]
                no_complaints=[]
                emp_id=[]

                table2=dynamodb.Table('employees')
                response3=table2.scan()

                for dic in response3['Items']:
                    if dic['active']==True and dic['org_id']==int(org_id):
                        name.append(dic['emp_name'])
                        department.append(dic['department'])
                        hierarchy.append(dic['hierarchy'])
                        no_complaints.append(dic['no_complaints'])
                        emp_id.append(dic['emp_id'])

                info_list=zip(name,department,hierarchy,no_complaints,emp_id)

                context={
                    'info_list':info_list,
                    'org_id':org_id,
                    'dep':dep,
                    'present':present,
                    'no_of_departments':no_of_departments,
                    'no_of_employees':no_of_employees,
                    'no_of_complaints':no_of_complaints,
                    'organisation_name':organisation_name

                }

                return render(request, 'employee/juniors.html',context)

            return render(request, 'employee/juniors.html',context)


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
        data={'complaint':zip(new_complaint,b,complaint_id),'count':len(new_complaint),'count_dealed':count_dealed,'count_date':count_date,'notification':notification,'org_id':j }

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
