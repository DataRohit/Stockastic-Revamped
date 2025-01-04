# Imports
from concurrent.futures import ThreadPoolExecutor, as_completed

from nsepython import nse_get_advances_declines, nse_get_top_gainers

from apps.socket.utils import fetch_and_process_quote


# Function to get top equity gainers quotes
def get_top_equity_gainers_quotes() -> dict[str, dict]:
    """Function to get top equity gainers quotes

    Returns:
        dict[str, dict]: Dictionary containing the quotes of top equity gainers
    """

    # Get the top gainers
    top_gainers = nse_get_top_gainers()["symbol"]

    # Dict to store the quotes
    quotes = {}

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=min(len(top_gainers), 4)) as executor:
        # Submit all the tasks at once and map results to indices
        future_to_index = {
            executor.submit(fetch_and_process_quote, f"{index}.NS"): index
            for index in top_gainers
        }

        # Process results as they complete instead of waiting for all
        for future in as_completed(future_to_index):
            # Get the index and data
            index, data = future.result()

            # If data is available
            if data:
                # Update the quotes
                quotes[index] = data

    # Return the dictionary
    return quotes


# Function to get top equity gainers 20 quotes
def get_top_equity_gainers_20_quotes(stock_exchange: str) -> dict[str, dict]:
    """Function to get top equity gainers 20 quotes

    Args:
        stock_exchange (str): Stock exchange to get the top equity gainers 20 quotes

    Returns:
        dict[str, dict]: Dictionary containing the quotes of top equity gainers 20
    """

    # Get the top gainers 22
    top_gainers = (
        nse_get_advances_declines()
        .sort_values(by="pChange", ascending=False)
        .head(22)["symbol"]
    )

    # Exchange symbol
    if stock_exchange == "NSE":
        exchange_symbol = "NS"
    elif stock_exchange == "BSE":
        exchange_symbol = "BO"

    # Dict to store the quotes
    quotes = {}

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=min(len(top_gainers), 4)) as executor:
        # Submit all the tasks at once and map results to indices
        future_to_index = {
            executor.submit(
                fetch_and_process_quote, f"{index}.{exchange_symbol}"
            ): index
            for index in top_gainers
        }

        # Process results as they complete instead of waiting for all
        for future in as_completed(future_to_index):
            # Get the index and data
            index, data = future.result()

            # If data is available and less than 20
            if data and len(quotes) < 20:
                # Update the quotes
                quotes[index] = data

    # Return the dictionary
    return quotes
