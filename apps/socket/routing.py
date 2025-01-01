# Imports
from django.urls import path

from apps.socket.consumers import IndexQuotesConsumer, TopIndexQuotesConsumer

websocket_urlpatterns = [
    path("ws/topIndexQuotes/", TopIndexQuotesConsumer.as_asgi(), name="topIndexQuotes"),
    path("ws/indexQuotes/", IndexQuotesConsumer.as_asgi(), name="indexQuotes"),
]
