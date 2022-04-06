import json
# noinspection PyUnresolvedReferences
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from pprint import pprint
from . import models, forms


class StateConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        pprint(self.scope['url_route'])
        pprint(self.scope['url_route']['kwargs'])
        pprint(self.scope['url_route']['kwargs']['loja'])

        self.room_name = self.scope['url_route']['kwargs']['loja']
        self.room_group_name = 'channel_%s' % self.room_name

        # Join room group de pedidos
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print("Dentro")

    async def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(data)
        stt = response.post("stats", None)
        ped = response.post("idstat", None)

        statusatualizado=''
        if ped :
            # enviar para o feed o status do pedido atualizado
            # print(request.POST)
            pedid = models.Pedido.objects.get(pk=ped)
            # pprint(ped)
            pedid.status = stt
            p = pedid.save(commit=False)
            await self.channel_layer.group_send(self.room_group_name, {
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

