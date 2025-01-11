# Imports
from typing import Any, Dict

import yfinance as yf


# Function to fetch the ticker data
def fetch_ticker_data(
    ticker: yf.Ticker, data_type: str, period: str = "1d", interval: str = "5m"
) -> Dict[str, Any]:
    """Fetch specific ticker data type (info or fast_info)

    Args:
        ticker (yf.Ticker): Ticker object
        data_type (str): Type of data to fetch ('info' or 'fast_info' or 'history')

    Returns:
        Dict[str, Any]: Fetched data
    """

    # If data type is history
    if data_type == "history":
        # Fetch the historical data
        return ticker.history(period=period, interval=interval)[
            ["Open", "High", "Low", "Close"]
        ]

    # If data type is info
    elif data_type == "info":
        # Return the info data
        return dict(ticker.info)

    # If data type is fast_info
    elif data_type == "fast_info":
        # Return the fast_info data
        return dict(ticker.fast_info)

    # Return an empty dict
    return {}
