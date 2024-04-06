from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/feedbacks/(?P<pk>\d+)/$', consumers.FeedbacksConsumer.as_asgi()),
]