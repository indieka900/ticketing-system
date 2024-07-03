# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from .services import consumers

websocket_urlpatterns = [
    path('ws/feedbacks/<int:pk>/', consumers.FeedbackConsumer),
    # Define other WebSocket paths here if needed
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
