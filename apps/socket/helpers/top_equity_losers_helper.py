# Imports
from concurrent.futures import ThreadPoolExecutor, as_completed

from nsepython import nse_get_advances_declines, nse_get_top_losers

from apps.socket.utils import fetch_and_process_quote


# Function to get top equity losers quotes
def get_top_equity_losers_quotes() -> dict[str, dict]:
    """Function to get top equity losers quotes

    Returns:
        dict[str, dict]: Dictionary containing the quotes of top equity losers
    """

    # Get the top losers
    top_losers = nse_get_top_losers()["symbol"]

    # Dict to store the quotes
    quotes = {}

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=min(len(top_losers), 4)) as executor:
        # Submit all the tasks at once and map results to indices
        future_to_index = {
            executor.submit(fetch_and_process_quote, f"{index}.NS"): index
            for index in top_losers
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


# Function to get top equity losers 20 quotes
def get_top_equity_losers_20_quotes(stock_exchange: str) -> dict[str, dict]:
    """Function to get top equity losers 20 quotes

    Args:
        stock_exchange (str): Stock exchange to get the top equity losers 20 quotes

    Returns:
        dict[str, dict]: Dictionary containing the quotes of top equity losers 20
    """

    # Get the top losers 20
    top_losers = (
        nse_get_advances_declines()
        .sort_values(by="pChange", ascending=True)
        .head(20)["symbol"]
    )

    # Exchange symbol
    if stock_exchange == "NSE":
        exchange_symbol = "NS"
    elif stock_exchange == "BSE":
        exchange_symbol = "BO"

    # Dict to store the quotes
    quotes = {}

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=min(len(top_losers), 4)) as executor:
        # Submit all the tasks at once and map results to indices
        future_to_index = {
            executor.submit(
                fetch_and_process_quote, f"{index}.{exchange_symbol}"
            ): index
            for index in top_losers
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
