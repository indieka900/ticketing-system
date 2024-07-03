from channels.generic.websocket import AsyncWebsocketConsumer

class FeedbackConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.pk = self.scope['url_route']['kwargs']['pk']
        await self.channel_layer.group_add(
            f'feedbacks_{self.pk}',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f'feedbacks_{self.pk}',
            self.channel_name
        )

    async def new_feedback(self, event):
        # Send new feedback to WebSocket clients
        await self.send(text_data=event['text'])
