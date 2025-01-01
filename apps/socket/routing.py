# Imports
from django.urls import path

from apps.socket.consumers import (
    IndexQuotesConsumer,
    QuoteChartConsumer,
    QuoteConsumer,
    TopIndexQuotesConsumer,
)

websocket_urlpatterns = [
    path("ws/topIndexQuotes/", TopIndexQuotesConsumer.as_asgi(), name="topIndexQuotes"),
    path("ws/indexQuotes/", IndexQuotesConsumer.as_asgi(), name="indexQuotes"),
    path(
        "ws/quote/<str:symbol>/",
        QuoteConsumer.as_asgi(),
        name="indexQuoteWithSymbol",
    ),
    path(
        "ws/quote/<str:symbol>/chart/",
        QuoteChartConsumer.as_asgi(),
        name="indexQuoteWithSymbolChart",
    ),
]
