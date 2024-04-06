from channels.generic.websocket import AsyncWebsocketConsumer
import json

class FeedbacksConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.complaint_id = self.scope['url_route']['kwargs']['pk']
        self.group_name = f'feedbacks_{self.complaint_id}'

        # Join the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']
        file = text_data_json['file']

        # Send message to the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'new_feedback',
                'message': message,
                'sender': sender,
                'receiver': receiver,
                'file': file
            }
        )

    # Receive message from group
    async def new_feedback(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        file = event['file']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'receiver': receiver,
            'file': file
        }))