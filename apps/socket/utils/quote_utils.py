# Imports
import math
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Optional, Tuple

import yfinance as yf

from apps.socket.constants import REQUIRED_FIELDS

from .ticker_utils import fetch_ticker_data


# Function to process the quote
def process_quote(quote: Dict) -> Dict:
    """Process quote with all calculations

    Args:
        quote (Dict): The quote dictionary

    Returns:
        Dict: Processed quote dictionary
    """

    # Calculate changes in one pass
    last_price = quote["lastPrice"]
    prev_close = quote["previousClose"]
    day_change = last_price - prev_close

    # Update dictionary with all changes at once
    quote.update(
        {
            "dayChange": day_change,
            "dayChangePercentage": (
                (day_change / prev_close * 100) if prev_close != 0 else 0
            ),
            "colorClass": "text-green-500" if day_change >= 0 else "text-red-500",
        }
    )

    # Return the quote
    return quote


# Function to process the quote data
def fetch_and_process_quote(
    symbol: str,
    filter: bool = True,
) -> Tuple[str, Optional[Dict]]:
    """Fetch and process data using concurrent execution

    Args:
        symbol (str): Stock symbol
        filter (bool, optional): Flag to filter the data. Defaults to True.

    Returns:
        Tuple[str, Optional[Dict]]: Tuple containing the symbol and processed data
    """

    # Try
    try:
        # Get the ticker object
        item_ticker = yf.Ticker(symbol)

        # Create ThreadPoolExecutor for concurrent fetching
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Submit both fetch tasks
            future_info = executor.submit(fetch_ticker_data, item_ticker, "info")
            future_fast_info = executor.submit(
                fetch_ticker_data, item_ticker, "fast_info"
            )

            # Get results from both futures
            info = future_info.result()
            info_fast = future_fast_info.result()

            # Combine the info with priority to fast_info
            result = {**info_fast, **info}

            # If filter
            if filter:
                # Filter and process the data
                result = {key: result.get(key) for key in REQUIRED_FIELDS}

            # Replace all nan values with None
            result = {
                key: None if isinstance(value, float) and math.isnan(value) else value
                for key, value in result.items()
            }

            # Process the quote data
            result = process_quote(result)

            # Return the symbol and result
            return symbol, result

    # If error
    except Exception as e:
        # Print the error
        print(f"Error processing index {symbol}: {e}")

        # Return the symbol and None
        return symbol, None
