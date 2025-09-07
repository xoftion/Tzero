import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from orders.models import Order
from users.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'chat_{self.order_id}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        is_authorized = await self.is_user_authorized(self.user, self.order_id)
        if not is_authorized:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save message to database
        await self.save_message(self.user, self.order_id, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author': self.user.username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        author = event['author']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author
        }))

    @database_sync_to_async
    def is_user_authorized(self, user, order_id):
        try:
            order = Order.objects.select_related('buyer', 'items__product__seller').get(id=order_id)
            seller = order.items.first().product.seller
            return user == order.buyer or user == seller
        except Order.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, author, order_id, content):
        order = Order.objects.get(id=order_id)
        Message.objects.create(author=author, order=order, content=content)
