from cgitb import text
from email import message
import json
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

from EscalArt.models import Chat, ChatRoom

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.user_idUser = self.scope['user'].idUser

        # encuentra sala(room) object
        room = await database_sync_to_async(ChatRoom.objects.get)(nombre=self.room_name)

        # Crea nuevo chat object
        chat = Chat(
            contenido=message,
            idUser=self.scope['user'],
            room=room
        )
        await database_sync_to_async(chat.save)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'user_idUser':self.user_idUser
            }
        )

    async def chat_message(self,event):
        message = event['message']
        user_idUser = event['user_idUser']
        await self.send(text_data = json.dumps({
            'message':message,
            'user_idUser':user_idUser
        }))

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
        
#         self.user_idUser = self.scope['user'].idUser

#          # encuentra sala(room) object
#         room = await database_sync_to_async(ChatRoom.objects.get)(nombre=self.room_name)

#         # Crea nuevo chat object
#         chat = Chat(
#             contenido=message,
#             idUser=self.scope['user'],
#             room=room
#         )
#         await database_sync_to_async(chat.save)()

#         await self.send(text_data=json.dumps({
#             'message':message,
#             'user_idUser':self.user_idUser
#         }))
#         # await self.send(
#         #     self.room_group_name,
#         #     {
#         #         'type':'chat_message',
#         #         'message':message,
#         #         'user_idUser':self.user_idUser
#         #     }
#         # )

#     async def chat_message(self,event):
#         message = event['message']
#         user_idUser = event['user_idUser']
#         await self.send(text_data = json.dumps({
#             'message':message,
#             'user_idUser':user_idUser
#         }))