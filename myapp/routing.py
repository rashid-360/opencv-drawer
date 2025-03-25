# myapp/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('socketmsg/', consumers.SomeConsumer.as_asgi()),
    # Define other WebSocket endpoints and consumers here
]
