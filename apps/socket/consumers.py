# Imports
import json

import anyio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps

from apps.socket.helpers import (
    generate_candlestick_chart,
    get_bookmarked_quotes,
    get_index_quotes,
    get_quote,
    get_top_equity_gainers_20_quotes,
    get_top_equity_gainers_quotes,
    get_top_equity_losers_20_quotes,
    get_top_equity_losers_quotes,
    get_top_index_quotes,
)


# TopIndexQuotesConsumer class
class TopIndexQuotesConsumer(AsyncWebsocketConsumer):
    # Connect method
    async def connect(self):
        # Accept the connection
        await self.accept()

        # Flag to control the updates
        self.keep_sending = True

        # Send initial data when connection is established
        await self.send_quotes()

    # Disconnect method
    async def disconnect(self, close_code):
        # Stop sending updates on disconnect
        self.keep_sending = False

    # Receive method
    async def send_quotes(self):
        # Try
        try:
            # Send data to the WebSocket client
            while self.keep_sending:
                # Fetch the top index quotes
                quotes_dict = get_top_index_quotes()

                # Send the quotes to the WebSocket client
                await self.send(json.dumps(quotes_dict))

                # Wait for 2.0 second before sending the next update
                await anyio.sleep(2.0)

        # If any exception occurs
        except Exception as e:
            # Print the error
            print(f"Error in send_quotes: {e}")

            # Stop sending updates
            self.keep_sending = False


# IndexQuotesConsumer class
class IndexQuotesConsumer(AsyncWebsocketConsumer):
    # Connect method
    async def connect(self):
        # Accept the connection
        await self.accept()

        # Parse query parameters from the connection scope
        self.query_params = self.parse_query_string(self.scope["query_string"])

        # Flag to control the updates
        self.keep_sending = True

        # Send initial data when connection is established
        await self.send_quotes()

    # Disconnect method
    async def disconnect(self, close_code):
        # Stop sending updates on disconnect
        self.keep_sending = False

    # Receive method
    async def send_quotes(self):
        # Try
        try:
            # Send data to the WebSocket client
            while self.keep_sending:
                # Get values from the query parameters
                stock_exchange = self.query_params.get("stock_exchange", "NSE")
                category = self.query_params.get("category", "broad-market")

                # Fetch the index quotes
                quotes_dict = get_index_quotes(stock_exchange, category)

                # Send the quotes to the WebSocket client
                await self.send(json.dumps(quotes_dict))

                # Wait for 2.0 second before sending the next update
                await anyio.sleep(2.0)

        # If any exception occurs
        except Exception as e:
            # Print the error
            print(f"Error in send_quotes: {e}")

            # Stop sending updates
            self.keep_sending = False

    # Static method to parse query string
    @staticmethod
    def parse_query_string(query_string: bytes) -> dict:
        """Parse the query string and return the query parameters as a dictionary.

        Args:
            query_string (bytes): The query string from the connection scope.

        Returns:
            dict: The query parameters as a dictionary.
        """

        # Import the required function
        from urllib.parse import parse_qs

        # Decode and parse the query string
        query_params = parse_qs(query_string.decode())

        # Convert list values to single values (assuming single-value params)
        return {key: value[0] for key, value in query_params.items()}


# QuoteConsumer class
class QuoteConsumer(AsyncWebsocketConsumer):
    # Connect method
    async def connect(self):
        # Accept the connection
        await self.accept()

        # Extract the symbol from the URL
        self.symbol = self.scope["url_route"]["kwargs"]["symbol"]

        # Flag to control the updates
        self.keep_sending = True

        # Send initial data when connection is established
        await self.send_quote()

    # Disconnect method
    async def disconnect(self, close_code):
        # Stop sending updates on disconnect
        self.keep_sending = False

    # Receive method
    async def send_quote(self):
        # Try
        try:
            # Send data to the WebSocket client
            while self.keep_sending:
                # Fetch the index quotes
                quote = get_quote(self.symbol)

                # Send the quotes to the WebSocket client
                await self.send(json.dumps(quote))

                # Wait for 2.0 second before sending the next update
                await anyio.sleep(2.0)

        # If any exception occurs
        except Exception as e:
            # Print the error
            print(f"Error in send_quote: {e}")

            # Stop sending updates
            self.keep_sending = False


# QuoteChartConsumer class
class QuoteChartConsumer(AsyncWebsocketConsumer):
    # Connect method
    async def connect(self):
        # Accept the connection
        await self.accept()

        # Extract the symbol from the URL
        self.symbol = self.scope["url_route"]["kwargs"]["symbol"]

        # Flag to control the updates
        self.keep_sending = True

        # Send initial data when connection is established
        await self.send_quote()

    # Disconnect method
    async def disconnect(self, close_code):
        # Stop sending updates on disconnect
        self.keep_sending = False

    # Receive method
    async def send_quote(self):
        # Try
        try:
            # Send data to the WebSocket client
            while self.keep_sending:
                # Get the chart for the index quote
                chart = generate_candlestick_chart(self.symbol).to_html()

                # Send the quotes to the WebSocket client
                await self.send(chart)

                # Wait for 5.0 second before sending the next update
                await anyio.sleep(5.0)

        # If any exception occurs
        except Exception as e:
            # Print the error
            print(f"Error in send_quote: {e}")

            # Stop sending updates
            self.keep_sending = False


# TopEquityGainersQuotesConsumer class
class TopEquityGainersQuotesConsumer(AsyncWebsocketConsumer):
    # Connect method
    async def connect(self):
        # Accept the connection
        await self.accept()

        # Flag to control the updates
        self.keep_sending = True

        # Send initial data when connection is established
        await self.send_quotes()

    # Disconnect method
    async def disconnect(self, close_code):
        # Stop sending updates on disconnect
        self.keep_sending = False

    # Receive method
    async def send_quotes(self):
        # Try
        try:
            # Send data to the WebSocket client
            while self.keep_sending:
                # Fetch the top equity gainers quotes
                quotes_dict = get_top_equity_gainers_quotes()

                # Send the quotes to the WebSocket client
                await self.send(json.dumps(quotes_dict))

                # Wait for 2.0 second before sending the next update
                await anyio.sleep(2.0)

        # If any exception occurs
        except Exception as e:
            # Print the error
            print(f"Error in send_quotes: {e}")

            # Stop sending updates
            self.keep_sending = False


# TopEquityLosersQuotesConsumer class
class TopEquityLosersQuotesConsumer(AsyncWebsocketConsumer):
    # Connect method
    async def connect(self):
        # Accept the connection
        await self.accept()

        # Flag to control the updates
        self.keep_sending = True

        # Send initial data when connection is established
        await self.send_quotes()

    # Disconnect method
    async def disconnect(self, close_code):
        # Stop sending updates on disconnect
        self.keep_sending = False

    # Receive method
    async def send_quotes(self):
        # Try
        try:
            # Send data to the WebSocket client
            while self.keep_sending:
                # Fetch the top equity losers quotes
                quotes_dict = get_top_equity_losers_quotes()

                # Send the quotes to the WebSocket client
                await self.send(json.dumps(quotes_dict))

                # Wait for 2.0 second before sending the next update
                await anyio.sleep(2.0)

        # If any exception occurs
        except Exception as e:
            # Print the error
            print(f"Error in send_quotes: {e}")

            # Stop sending updates
            self.keep_sending = False


# TopEquityGainersQuotes20Consumer class
class TopEquityGainersQuotes20Consumer(AsyncWebsocketConsumer):
    # Connect method
    async def connect(self):
        # Accept the connection
        await self.accept()

        # Parse query parameters from the connection scope
        self.query_params = self.parse_query_string(self.scope["query_string"])

        # Flag to control the updates
        self.keep_sending = True

        # Send initial data when connection is established
        await self.send_quotes()

    # Disconnect method
    async def disconnect(self, close_code):
        # Stop sending updates on disconnect
        self.keep_sending = False

    # Receive method
    async def send_quotes(self):
        # Try
        try:
            # Send data to the WebSocket client
            while self.keep_sending:
                # Get values from the query parameters
                stock_exchange = self.query_params.get("stock_exchange", "NSE")

                # Fetch the top equity gainers quotes
                quotes_dict = get_top_equity_gainers_20_quotes(stock_exchange)

                # Send the quotes to the WebSocket client
                await self.send(json.dumps(quotes_dict))

                # Wait for 2.0 second before sending the next update
                await anyio.sleep(2.0)

        # If any exception occurs
        except Exception as e:
            # Print the error
            print(f"Error in send_quotes: {e}")

            # Stop sending updates
            self.keep_sending = False

    # Static method to parse query string
    @staticmethod
    def parse_query_string(query_string: bytes) -> dict:
        """Parse the query string and return the query parameters as a dictionary.

        Args:
            query_string (bytes): The query string from the connection scope.

        Returns:
            dict: The query parameters as a dictionary.
        """

        # Import the required function
        from urllib.parse import parse_qs

        # Decode and parse the query string
        query_params = parse_qs(query_string.decode())

        # Convert list values to single values (assuming single-value params)
        return {key: value[0] for key, value in query_params.items()}


# TopEquityLosersQuotes20Consumer class
class TopEquityLosersQuotes20Consumer(AsyncWebsocketConsumer):
    # Connect method
    async def connect(self):
        # Accept the connection
        await self.accept()

        # Parse query parameters from the connection scope
        self.query_params = self.parse_query_string(self.scope["query_string"])

        # Flag to control the updates
        self.keep_sending = True

        # Send initial data when connection is established
        await self.send_quotes()

    # Disconnect method
    async def disconnect(self, close_code):
        # Stop sending updates on disconnect
        self.keep_sending = False

    # Receive method
    async def send_quotes(self):
        # Try
        try:
            # Send data to the WebSocket client
            while self.keep_sending:
                # Get values from the query parameters
                stock_exchange = self.query_params.get("stock_exchange", "NSE")

                # Fetch the top equity losers quotes
                quotes_dict = get_top_equity_losers_20_quotes(stock_exchange)

                # Send the quotes to the WebSocket client
                await self.send(json.dumps(quotes_dict))

                # Wait for 2.0 second before sending the next update
                await anyio.sleep(2.0)

        # If any exception occurs
        except Exception as e:
            # Print the error
            print(f"Error in send_quotes: {e}")

            # Stop sending updates
            self.keep_sending = False

    # Static method to parse query string
    @staticmethod
    def parse_query_string(query_string: bytes) -> dict:
        """Parse the query string and return the query parameters as a dictionary.

        Args:
            query_string (bytes): The query string from the connection scope.

        Returns:
            dict: The query parameters as a dictionary.
        """

        # Import the required function
        from urllib.parse import parse_qs

        # Decode and parse the query string
        query_params = parse_qs(query_string.decode())

        # Convert list values to single values (assuming single-value params)
        return {key: value[0] for key, value in query_params.items()}


# BookmarkQuotes class
class BookmarkQuotes(AsyncWebsocketConsumer):
    # Connect method
    async def connect(self):
        # Accept the connection
        await self.accept()

        # Extract the customer_id from the URL
        self.customer_id = self.scope["url_route"]["kwargs"]["customer_id"]

        # Flag to control the updates
        self.keep_sending = True

        # Send initial data when connection is established
        await self.send_quotes()

    # Disconnect method
    async def disconnect(self, close_code):
        # Stop sending updates on disconnect
        self.keep_sending = False

    # Receive method
    async def send_quotes(self):
        # Try
        try:
            # Send data to the WebSocket client
            while self.keep_sending:
                # Get the model only when needed, not at module level
                StockIndexWatchlist = apps.get_model("dashboard", "StockIndexWatchlist")

                # Fetch the stock index watchlist for the customer
                watchlist = await self.get_watchlist(
                    StockIndexWatchlist, self.customer_id
                )

                # Get list of symbols
                symbols = [item.symbol for item in watchlist]

                # Get the quotes
                quotes = get_bookmarked_quotes(symbols)

                # Send the quotes to the WebSocket client
                await self.send(json.dumps(quotes))

                # Wait for 2.0 second before sending the next update
                await anyio.sleep(2.0)

        # If any exception occurs
        except Exception as e:
            # Print the error
            print(f"Error in send_quotes: {e}")

            # Stop sending updates
            self.keep_sending = False

    # Static method to get watchlist
    @staticmethod
    async def get_watchlist(StockIndexWatchlist, customer_id):
        """Get watchlist using database model.

        This method is separated to handle the async database query properly.
        """

        # Use sync_to_async since Django ORM queries are synchronous
        from asgiref.sync import sync_to_async

        # Get the watchlist
        get_watchlist = sync_to_async(
            lambda: list(
                StockIndexWatchlist.objects.filter(user__id=customer_id).order_by(
                    "-type", "symbol"
                )
            )
        )

        # Return the watchlist
        return await get_watchlist()
