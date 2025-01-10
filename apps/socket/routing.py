# Imports
from django.urls import path

from apps.socket.consumers import (
    BookmarkQuotes,
    IndexQuotesConsumer,
    QuoteChartConsumer,
    QuoteConsumer,
    TopEquityGainersQuotes20Consumer,
    TopEquityGainersQuotesConsumer,
    TopEquityLosersQuotes20Consumer,
    TopEquityLosersQuotesConsumer,
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
    path(
        "ws/topEquityGainersQuotes/",
        TopEquityGainersQuotesConsumer.as_asgi(),
        name="topEquityGainersQuotes",
    ),
    path(
        "ws/topEquityLosersQuotes/",
        TopEquityLosersQuotesConsumer.as_asgi(),
        name="topEquityLosersQuotes",
    ),
    path(
        "ws/topEquityGainersQuotes20/",
        TopEquityGainersQuotes20Consumer.as_asgi(),
        name="topEquityGainersQuotes20",
    ),
    path(
        "ws/topEquityLosersQuotes20/",
        TopEquityLosersQuotes20Consumer.as_asgi(),
        name="topEquityLosersQuotes20",
    ),
    path(
        "ws/<str:customer_id>/bookmarkQuotes/",
        BookmarkQuotes.as_asgi(),
        name="bookmarkQuotes",
    ),
]
