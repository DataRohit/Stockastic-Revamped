# Imports
import json

import anyio
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.socket.helpers import get_top_index_quotes


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
