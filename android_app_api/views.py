from django.shortcuts import render
from rest_framework.decorators import renderer_classes
from rest_framework.response import Response
from .token_auth_decorator import api_view , token_auth
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import hashlib
import random
import string
from datetime import datetime
from datetime import timedelta



dynamodb = boto3.resource('dynamodb')


@api_view(["GET"])
def getMyActiveComplaints(req):
    if ('HTTP_AUTHORIZATION' in req.META):
        print("HOLA")
        table = dynamodb.Table("AndroidUserPrimaryTokens")
        token = req.META['HTTP_AUTHORIZATION']
        resp = table.scan(
            FilterExpression=Attr('tokken').eq(token)
        )
        if resp["Count"] == 1 :
            genDate = resp["Items"][0]['timestamp']
            if datetime.strptime(genDate, "%y%m%d%H%M%S") + timedelta(minutes=10) > datetime.now() :
                return Response(
                            {
                                "data" : "You Can Fetch Data now"
                            }
                )
            table.delete_item(
                Key = {
                    'tokken' : token,
                }                
            )
            print("Amigo")
            return Response(
                {
                'status'  : 205
                }
            )
        print("real")
        return Response(
                {
                'status'  : 203
                }
        )
    return Response(
        {
                
        }
    )



@api_view(['GET'])
def get_org(req):
    if req.method == 'GET':
        if 'token' in req.method:
            pageSize = 25
            startIndex = 0
            table = dynamodb.Table('organization')
            Response0 = table.scan(
                ProjectionExpression="organization_name,org_id"
            )
            print(req.GET)
            if 'pageSize' in req.GET:
                pageSize = int(req.GET['pageSize'])
                print(pageSize)

            if 'startIndex' in req.GET:
                startIndex = int(req.GET['startIndex'])

            result = Response0['Items']

            if int(Response0['Count']) > pageSize+startIndex:
                print("in")
                result = result[startIndex: startIndex+pageSize]
            elif int(Response0['Count']) > startIndex:
                result = result[startIndex:]
            elif startIndex >= int(Response0['Count']):
                result = {}
            return Response(result)
        return Response({})


@api_view(["GET"])
def get_Complaint_Form(req):
    table = dynamodb.Table('Complaint_forms')
    response1 = table.scan(
        FilterExpression=Attr('form_id').eq('testform1')
    )
    return Response(response1['Items'])


@api_view(['POST'])
def complaint_form_add(req):
    if req.method == 'POST':

        table = dynamodb.Table('Complaint_forms')
        response1 = table.scan()
        f_id = len(response1['Items'])+1
        data = {'form_id': "testform"+str(f_id)}
        count = 0
        form0 = json.loads(req.data['data'])
        for element in form0:
            if element == "org_id":
                data.update({"org_id": str(form0[element]) })

            elif (form0[element] != "") and (element != "nE"):
                data.update({'field'+str(count): json.dumps(form0[element])})
                count += 1
        table.put_item(
            Item=data
        )
        return Response(data)
    print("fail")
    return Response(data)


@api_view(["POST"])
def getTokenPair(req):
    table = dynamodb.Table('users')
    print(req.data)
    print(req.POST)
    if('email'  in req.data  and  'password'  in req.data):
        email = req.data['email']
        pswd = req.data['password']
        table = dynamodb.Table('users')
        pswd = hashlib.sha256(pswd.encode())
        pswd = pswd.hexdigest()
        if (email != "" and pswd != ""):
            response = table.scan(
                ProjectionExpression="email,password,organizations_created,organizations_joined,username",
                FilterExpression=Attr('email').eq(email)
            )
            if (response['Count'] == 1):
                timestamp1 = datetime.now().strftime('%y%m%d%H%M%S')
                timestamp2 = datetime.now().strftime('%y%m%d%H%M%S')
                if pswd == response['Items'][0]['password']:
                    token = randomStringDigits() + timestamp1
                   

                    table = dynamodb.Table('AndroidUserPrimaryTokens')

                    table.put_item(
                        Item={
                            "tokken": token,
                            "timestamp": timestamp1,
                            "user": email,
                        }
                    )
                    
                    refresh = randomStringDigits() + timestamp2

                    table = dynamodb.Table('AndroidUserRefreshTokens')

                    table.put_item(
                        Item={
                            "refresh_tokken": refresh,
                            "timestamp": timestamp2,
                            "user": email,
                        }
                    )

                    return Response({
                        "token": token,
                        "refresh_tokken": refresh,
                        "status": 200,
                        "message": "Successful",
                    })
                
                return Response({
                    "status": 1,
                    "message" : "Incorrect Password or UserName",
                })

    return Response({
                    "message": "invalid inputs",
                    "status": 203
                    })
                
@api_view(['POST'])
def get_access_token(req):

    if 'refresh_token' in req.data:
        refresh_token = req.data['refresh_token']
        table = dynamodb.Table('AndroidUserRefreshTokens')
        response = table.scan(
            FilterExpression=Attr('refresh_tokken').eq(refresh_token)
        )
        if (response['Count'] == 1):

            timestamp1 = datetime.datetime.now().strftime('%y%m%d%H%M%S')
            token = randomStringDigits() + timestamp1

            table = dynamodb.Table('AndroidUserPrimaryTokens')

            table.put_item(
                Item={
                    "tokken": token,
                    "timestamp": timestamp1,
                    "user": email,
                }
            )
            return Response(
                {
                    "token": token,
                    "status": 201,
                    "message": "Successful",
                }
            )
        return Response(
            {
                "status": 202,
            }
        )
    return Response(
        {"status": 203}
    )

def randomStringDigits(stringLength=16):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


@api_view(['GET'])
def myComplaintHistory(req):
    if ('HTTP_AUTHORIZATION' in req.META):
            table = dynamodb.Table("AndroidUserPrimaryTokens")
            token = req.META['HTTP_AUTHORIZATION']
            resp = table.scan(
                FilterExpression=Attr('tokken').eq(token)
            )
            if resp["Count"] == 1 :
                genDate = resp["Items"][0]['timestamp']
                if datetime.strptime(genDate, "%y%m%d%H%M%S") + timedelta(minutes=10) > datetime.now() :
                    return Response(
                                {
                                    "data" : "You Can Fetch Data now"
                                }
                    )
                table.delete_item(
                    Key = {
                        'tokken' : token,
                    }                
                )
                return Response(
                    {
                    'status'  : 205
                    }
                )
            return Response(
                    {
                    'status'  : 203
                    }
            )
    return Response(
        {
                
        }
    )

@api_view(['GET'])
def get_Complaint_Detail(req):
    if ('token' in req.GET and 'complaint_id' in req.GET):
            table = dynamodb.Table("AndroidUserPrimaryTokens")
            token = req.GET['token']
            resp = table.scan(
                FilterExpression=Attr('tokken').eq(token)
            )
            if resp["Count"] == 1 :
                genDate = resp["Items"][0]['timestamp']
                if datetime.strptime(genDate, "%y%m%d%H%M%S") + timedelta(minutes=10) > datetime.now() :
                    return fun()
                table.delete_item(
                    Key = {
                        'tokken' : token,
                    }                
                )
                return Response(
                    {
                    'status'  : 205
                    }
                )
            return Response(
                    {
                    'status'  : 203
                    }
            )
    return Response(
        {
                
        }
    )
    