# Imports
from django.urls import path

from apps.socket.consumers import TopIndexQuotesConsumer

websocket_urlpatterns = [
    path("ws/topIndexQuotes/", TopIndexQuotesConsumer.as_asgi(), name="topIndexQuotes"),
]