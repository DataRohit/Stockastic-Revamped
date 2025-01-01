# Imports
from concurrent.futures import ThreadPoolExecutor, as_completed

from apps.socket.constants import STOCK_INDICES
from apps.socket.utils import fetch_and_process_quote


# Function to get index quotes
def get_index_quotes(stock_exchange: str, category: str) -> dict[str, dict]:
    """Function to get index quotes

    Args:
        stock_exchange (str): Stock exchange
        category (str): Category

    Returns:
        dict[str, dict]: Dictionary containing the quotes of indices
    """

    # Get the indices
    indices = STOCK_INDICES.get(stock_exchange, "NSE").get(category, "broad-market")

    # Dict to store the quotes
    quotes = {}

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=min(len(indices), 4)) as executor:
        # Submit all tasks at once and map results to indices
        future_to_index = {
            executor.submit(fetch_and_process_quote, index): index for index in indices
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
