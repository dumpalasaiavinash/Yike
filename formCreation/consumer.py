import asyncio
import json
import os
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from django.conf import settings
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

class formsaveConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connect")
        await self.send({
            "type": "websocket.accept"
        })
    async def websocket_disconnect(self, event):
        print("disconnected", event)
    
    async def websocket_receive(self, event):
        print("receive", event)

   
