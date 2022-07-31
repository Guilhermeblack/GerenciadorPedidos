import json
# noinspection PyUnresolvedReferences
import sys
from os import stat

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from pprint import pprint
from . import models, forms
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async



class StateConsumer(AsyncJsonWebsocketConsumer):



    async def connect(self):

        # pprint(self.scope['url_route']['kwargs'])
        # pprint(self.scope['url_route']['kwargs']['loja'])

        self.room_name = self.scope['url_route']['kwargs']['loja']
        self.room_group_name = 'loja_%s' % self.room_name
        # pprint(self.room_group_name)

        # pprint(self.room_name)
        # pprint(self.channel_name)
        # Join room group de pedidos
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        # print("Dentro")
        await self.accept()


    async def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        # pprint(response)
        # dir(response)
        stt = response['stats']
        ped = response['idstat']

        statusatualizado=''
        # if ped :
            # enviar para o feed o status do pedido atualizado

            # await sync_to_async(models.Pedido.objects.filter(pk=ped).update(status=stt), thread_sensitive=True)

        # print('foiaqanttt')
        await att_ped(response)
        await self.channel_layer.group_send(self.room_name, {
            'type':'send_message',

            'id': ped,
            'stat': stt,

        })



    async def send_message(self, res):
        # Send message to WebSocket

        await self.send(text_data=json.dumps({
            'id':res['id'],
            "stat": res["stat"],
        }))

@database_sync_to_async
def att_ped( dt):

    pprint(dt)

    ret_alt_status = models.Pedido.objects.get(pk=dt['idstat'])
    ret_alt_status.status = dt['stats']
    ret_alt_status.save()
    # return ree
