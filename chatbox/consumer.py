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


class msgConsumer(AsyncConsumer):
    @database_sync_to_async
    def sendMessage(self,sender, reciver,msg,date0,date1):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('messages')
        
        response1 = table.scan()
        u_id = len(response1['Items'])+1
        table.put_item(
            Item={
                'msg_id': str(u_id),
                'sort_key':str(date1),
                'messages': msg,
                'sender': sender,
                'reciver': reciver,
                'date_time': date0
            }
        )
        table = dynamodb.Table('lastmessage')
        response = table.scan(
            ProjectionExpression="msg_id,sender,reciver",
            FilterExpression=Attr('sender').eq(sender) or Attr('sender').eq(sender)
        )
        msg_id = 0
        if(response['Count'] == 1):
            msg_id = response['Items'][0]['msg_id']
            table.delete_item(
                Key={'msg_id': msg_id},
            )
        else:
            response = table.scan()
            msg_id = response['Count']

        table.put_item(
            Item={
                'msg_id': msg_id,
                'sender': sender,
                'reciver': reciver,
                'date_time': date0,
                'messages': msg,
            }
        )

    async def websocket_connect(self, event):
        print("connected", event)
        sender = self.scope['session']['email']
        reciver = self.scope['session']['rec']
        chatroom = await self.chatroom_id(sender, reciver)
        self.chatroom = chatroom
        await self.channel_layer.group_add(
            chatroom,
            self.channel_name
        )
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("receive", event)
        msg = event.get("text", None)
        if msg is not None:
            sender = self.scope['session']['email']
            reciver = self.scope['session']['rec']
            loaded_dict_data = json.loads(msg)
            message = loaded_dict_data.get('message')
            date2 = datetime.now()
            date0 = date2.strftime("%b %d \t|\t %H:%M")
            date1 = date2.strftime("%Y%m%d%H%M")

            msgres = {
                'message': message,
                'sender': sender,
                'reciver': reciver,
                'date_time':date0,
            }
            status = loaded_dict_data.get('status')
            stres = {
                'status': status,
                'sender': sender,
                'reciver': reciver
            }

            if msgres['message'] is not None:
                await self.sendMessage(sender, reciver, message,date0,date1)
                await self.channel_layer.group_send(self.chatroom, {
                    "type": "msgSend",
                    "text": json.dumps(msgres)
                })

            elif stres['status'] is not None:
                await self.channel_layer.group_send(self.chatroom, {
                    "type": "msgSend",
                    "text": json.dumps(stres)
                })

    async def msgSend(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']

        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def chatroom_id(self, me, rec):

        if True:
            return ("c"+me.replace('@', 'C')+"h"+rec.replace('@', 'C'))

        return ("d"+rec.replace('@', 'D')+"p"+me.replace('@', 'D'))

    