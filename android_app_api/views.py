from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import boto3
from boto3.dynamodb.conditions import Key, Attr

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }
    return Response(content)


@api_view(['PUT'])
def complaint_form_add(req):
    if req.method == 'PUT' :
        data = {}
        print(req.data)
        return Response(data)
    print("fail")
    return Response(data)
