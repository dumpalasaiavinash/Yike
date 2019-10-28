from django.shortcuts import render
from django.contrib import sessions
import copy
import boto3
from boto3.dynamodb.conditions import Key, Attr


# Create your views here.
def dashboard(request):
    # email=request.session['email']

    return render(request, 'dashboard/index.html')

def create(request):

    print(request.session['email'])

    # email="yashukikkuri@gmail.com"
    # dynamoDB=boto3.resource('dynamodb')
    # dynamoTable=dynamoDB.Table('users')
    #
    # response = dynamoTable.scan(
    #     ProjectionExpression="organizations_created,organizations_joined",
    #     FilterExpression=Attr('email').eq(email)
    # )
    #
    # print(response)
    # print('\n**\n')
    #
    # organizations_created=response['Items'][0]['organizations_created']
    # organizations_joined=response['Items'][0]['organizations_joined']
    # total_org_ids=copy.deepcopy(organizations_created)
    # for i in organizations_joined:
    #     total_org_ids.append(i)
    #     # topics=[]
    #     # print(codes)
    #     # dynamoTable=dynamoDB.Table('topics')
    #     # for index in range(0,len(codes)):
    #     #     response=dynamoTable.get_item(
    #     #     Key={
    #     #     'code':codes[index],
    #     #     }
    #     #     )
    #     #     print(response['Item']['topic'])
    #     #     topics+=[response['Item']['topic']]
    #     # print(topics)
    #
    # org_names=[]
    # dynamoTable=dynamoDB.Table('organization')
    # for i in total_org_ids:
    #     print(type(int(i)))
    #     response = dynamoTable.scan(
    #         ProjectionExpression="organization_name",
    #         FilterExpression=Attr('org_id').eq(int(i))
    #     )
    #     org_names.append(response['Items'][0]['organization_name'])
    # organizations_created_names=[]
    # organizations_joined_names=[]
    # count=0
    # for i in org_names:
    #     if(count>=len(organizations_created)):
    #         organizations_joined_names.append(i)
    #     else:
    #         organizations_created_names.append(i)
    #     count=count+1
    # print(organizations_joined_names)
    # print(organizations_created_names)
    #
    #
    # # dynamoDB=boto3.resource('dynamodb')
    # # dynamoTable=dynamoDB.Table('topics')
    # # response=dynamoTable.scan(
    # # )
    # # # print(response)
    # # # print("\n\n\n\n")
    # # # print(response['Items'])
    # # topics_created=[]
    # # codes_created=[]
    # # for index in response['Items']:
    # #     # print(index['name'])
    # #     # print(request.user.username)
    # #     if(index['name']==request.user.username):
    # #         topics_created+=[index['topic']]
    # #         codes_created+=[index['code']]
    # #
    # # print(codes_created)
    #
    #
    # extra = (len(organizations_created)%4)-1
    # data = {'topics' : zip(organizations_created_names,organizations_created), 'topics_created' : zip(organizations_joined_names,organizations_joined), 'topics_size' : len(organizations_created), 'topics_created_size' : len(organizations_joined), 'extra_grid' : extra}
    # return render(request, 'orgadmin/dummy.html', data)



def createform(request):
    return render(request,'orgadmin/createform.html')
