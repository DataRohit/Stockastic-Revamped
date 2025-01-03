# Imports
from concurrent.futures import ThreadPoolExecutor, as_completed

from nsepython import nse_get_top_gainers

from apps.socket.utils import fetch_and_process_quote


# Function to get top equity gainers quotes
def get_top_equity_gainers_quotes() -> dict[str, dict]:
    """Function to get top equity gainers quotes

    Returns:
        dict[str, dict]: Dictionary containing the quotes of top equity gainers
    """

    # Get the top gainers
    top_gainers = nse_get_top_gainers()["symbol"][:4]

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
