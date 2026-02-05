import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message
from visits.models import Visit

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        # Vérification sommaire de l'utilisateur (on affinera avec le middleware JWT)
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            # Rejoindre le groupe de la conversation
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recevoir un message du WebSocket (depuis Next.js)
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('type')

        if action == 'mark_as_read':
            reader = await self.mark_conversation_as_read()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'read_receipt',
                    'reader': reader
                }
            )
            return

        message_text = data.get('message', '')
        visit_id = data.get('visit_id') # Récupération de l'ID visite
        local_id = data.get('local_id')
        user = self.scope["user"]

        msg = await self.save_message(user, message_text, visit_id)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'id': msg.id,
                'message': message_text,
                'sender': user.username,
                'visit': await self.get_visit_data(msg), # On renvoie les infos de visite
                'local_id': local_id
            }
        )

    async def chat_message(self, event):
        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps(event))

    async def read_receipt(self, event):
        # Envoyer l'accusé de lecture au WebSocket
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def mark_conversation_as_read(self):
        user = self.scope["user"]
        Message.objects.filter(conversation_id=self.conversation_id).exclude(sender=user).update(is_read=True)
        return user.username

    @database_sync_to_async
    def save_message(self, user, text, visit_id=None):
        conv = Conversation.objects.get(id=self.conversation_id)
        visit_obj = None
        if visit_id:
            visit_obj = Visit.objects.get(id=visit_id)
        return Message.objects.create(conversation=conv, sender=user, text=text, visit=visit_obj)

    @database_sync_to_async
    def get_visit_data(self, msg):
        if msg.visit:
            return {
                'id': msg.visit.id,
                'proposed_date': msg.visit.proposed_date.isoformat(),
                'status': msg.visit.status
            }
        return None