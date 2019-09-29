from django.shortcuts import render
import boto3
from boto3.dynamodb.conditions import Key, Attr



# Create your views here.
def home(request):
    # if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('pass')
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('users')
    response = table.scan(
        ProjectionExpression="email,password",
        FilterExpression=Attr('email').eq(email)
    )
    print(response['Items'][0]['password'])
    if(len(response['Items'])>0):
        if(response['Items'][0]['password']==password):
            return render(request, 'home/home.html')
        else:
            return render(request, 'home/login.html')
    else:
        return render(request, 'home/signup.html')


def home_reg(request):
    # if request.method == 'POST':
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    re_password = request.POST.get('re_pass')
    print(password)
    print(re_password)
    if(password==re_password):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('users')
        response = table.scan(
            ProjectionExpression="email",
            FilterExpression=Attr('email').eq(username)
        )
        response1 = table.scan(ProjectionExpression="email")
        u_id=len(response1['Items'])+1
        print('\n')
        print(response)
        print('\n')
        print(response1)

        if(len(response['Items'])==0):
            response = table.put_item(
               Item={
                'u_id': u_id,
                'username': username,
                'email': email,
                'password': password,
                }
            )
            return render(request, 'home/home.html')

        else:
            return render(request, 'home/signup.html')
    else:
        return render(request, 'home/signup.html')



def login(request):
    return render(request, 'home/login.html')

def signup(request):
    return render(request, 'home/signup.html')
