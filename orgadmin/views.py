from django.shortcuts import render
from django.contrib import sessions
import copy
import boto3
from boto3.dynamodb.conditions import Key, Attr
import random


# Create your views here.
def dashboard(request):
    # email=request.session['email']

    if request.method=='POST':
        name=request.POST.get('emp_name')
        department=request.POST.get('department')
        hierarchy=request.POST.get('hierarchy')
        no_comp=request.POST.get('no_complaints')

        dynamodb=boto3.resource('dynamodb')
        table=dynamodb.Table('employees')

        response=table.scan
        response = table.scan(
                    ProjectionExpression="emp_id",
                )

        table.put_item(
            Item={
                'emp_id':len(response['Items'])+1,
                'emp_name':name,
                'department':department,
                'hierarchy':hierarchy,
                'no_complaints':no_comp,
            }
        )

    dynamodb=boto3.resource('dynamodb')
    table=dynamodb.Table('employees')
    response2=table.scan()

    name=[]
    department=[]
    hierarchy=[]
    no_complaints=[]

    print(response2['Items'])

    for dic in response2['Items']:
        name.append(dic['emp_name'])
        department.append(dic['department'])
        hierarchy.append(dic['hierarchy'])
        no_complaints.append(dic['no_complaints'])

    info_list=zip(name,department,hierarchy,no_complaints)

    context={
        "info_list":info_list,
    }


    return render(request, 'dashboard/index.html',context)

def form(request):
    return render(request,'dashboard/form.html')

def create(request):
    print(request.session['email'])

    email="yashukikkuri@gmail.com"
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('users')

    response = dynamoTable.scan(
        ProjectionExpression="organizations_created,organizations_joined",
        FilterExpression=Attr('email').eq(email)
    )

    print(response)
    print('\n**\n')

    organizations_created=response['Items'][0]['organizations_created']
    organizations_joined=response['Items'][0]['organizations_joined']
    total_org_ids=copy.deepcopy(organizations_created)
    for i in organizations_joined:
        total_org_ids.append(i)
        # topics=[]
        # print(codes)
        # dynamoTable=dynamoDB.Table('topics')
        # for index in range(0,len(codes)):
        #     response=dynamoTable.get_item(
        #     Key={
        #     'code':codes[index],
        #     }
        #     )
        #     print(response['Item']['topic'])
        #     topics+=[response['Item']['topic']]
        # print(topics)

    org_names=[]
    dynamoTable=dynamoDB.Table('organization')
    for i in total_org_ids:
        print(type(int(i)))
        response = dynamoTable.scan(
            ProjectionExpression="organization_name",
            FilterExpression=Attr('org_id').eq(int(i))
        )
        org_names.append(response['Items'][0]['organization_name'])
    organizations_created_names=[]
    organizations_joined_names=[]
    count=0
    for i in org_names:
        if(count>=len(organizations_created)):
            organizations_joined_names.append(i)
        else:
            organizations_created_names.append(i)
        count=count+1
    print(organizations_joined_names)
    print(organizations_created_names)


    # dynamoDB=boto3.resource('dynamodb')
    # dynamoTable=dynamoDB.Table('topics')
    # response=dynamoTable.scan(
    # )
    # # print(response)
    # # print("\n\n\n\n")
    # # print(response['Items'])
    # topics_created=[]
    # codes_created=[]
    # for index in response['Items']:
    #     # print(index['name'])
    #     # print(request.user.username)
    #     if(index['name']==request.user.username):
    #         topics_created+=[index['topic']]
    #         codes_created+=[index['code']]
    #
    # print(codes_created)
    colors=["linear-gradient(to right, rgba(255,0,0,0), rgba(255,0,0,1))","radial-gradient(circle, red, yellow, green)","linear-gradient(red, yellow)","linear-gradient(to bottom right, red, yellow)","linear-gradient(red, yellow, green)","linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(0,219,255,1) 47%)","linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(188,0,255,0.9080766095500701) 46%)","linear-gradient(90deg, rgba(131,58,180,1) 0%, rgba(253,153,29,1) 48%, rgba(252,176,69,1) 100%)"]
    colors1 = ["#ff4d4d", "#66ffff", "#1aff8c","#ff471a","#ffff33","#a3a375","#3333ff"]
    joined_color=[]
    created_color=[]

    for k in range(0,len(organizations_joined)):
        x=random.randint(0,7)
        joined_color.append(colors[x])
        print(x)

    for l in range(0,len(organizations_created)):
        y=random.randint(0,7)
        print(y)
        created_color.append(colors[x])

    print(created_color,x,joined_color)

    extra = (len(organizations_created)%4)-1
    data = {'topics' : zip(organizations_created_names,organizations_created,created_color), 'topics_created' : zip(organizations_joined_names,organizations_joined,joined_color), 'topics_size' : len(organizations_created), 'topics_created_size' : len(organizations_joined), 'extra_grid' : extra,'color_created':created_color,'color_joined':joined_color}
    return render(request, 'orgadmin/dummy.html', data)



def createform(request):
    return render(request,'orgadmin/createform.html')


def departments(request):

    organization_id = 105
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('departments')

    response = dynamoTable.scan(
        ProjectionExpression="department_name,department_id",
        FilterExpression=Attr('organization_id').eq(organization_id)
    )
    departments = []
    dep_id=[]
    for i in response['Items']:
        departments.append(i['department_name'])
        dep_id.append(i['department_id'])
    print(departments)

    return render(request,'orgadmin/org_departments.html',{'dep':zip(departments,dep_id)})



def hierarchy(request):
    res = request.POST.get('dep')
    print(res)
    data=res.split('_')
    dep_id=data[0]
    dep_name=data[1]
    return render(request,'orgadmin/departments.html',{'dep_name':dep_name,'dep_id':dep_id})



def departments_hierarchy_update(request,hierarchy):
    print(type(hierarchy))
    print(hierarchy)

    organization_id = 105
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('departments')

    response = dynamoTable.scan(
        ProjectionExpression="department_name,department_id",
        FilterExpression=Attr('organization_id').eq(organization_id)
    )
    departments = []
    dep_id=[]
    for i in response['Items']:
        departments.append(i['department_name'])
        dep_id.append(i['department_id'])
    print(departments)

    return render(request,'orgadmin/org_departments.html',{'dep':zip(departments,dep_id)})
