# Imports
from concurrent.futures import ThreadPoolExecutor, as_completed

from apps.socket.constants import TOP_INDICES
from apps.socket.utils import fetch_and_process_quote


# Function to get top index quotes
def get_top_index_quotes() -> dict[str, dict]:
    """Function to get top index quotes

    Returns:
        dict[str, dict]: Dictionary containing the quotes of top indices
    """

    # Dict to store the quotes
    quotes = {}

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=min(len(TOP_INDICES), 4)) as executor:
        # Submit all the tasks at once and map results to indices
        future_to_index = {
            executor.submit(fetch_and_process_quote, index): index
            for index in TOP_INDICES
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
