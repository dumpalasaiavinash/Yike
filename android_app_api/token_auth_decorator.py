import boto3
from rest_framework.decorators import api_view
from boto3.dynamodb.conditions import Key, Attr
from rest_framework.response import Response
from datetime import datetime
from datetime import timedelta
import types
from django.forms.utils import pretty_name
from rest_framework.views import APIView

def token_auth(fun):
    def wrapper_fun(*args,**kwargs):
        req = args[0]
        if ('token' in req.GET):
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
