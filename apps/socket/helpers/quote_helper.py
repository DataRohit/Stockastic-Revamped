# Imports
from apps.socket.utils import fetch_and_process_quote


# Function to get index quote
def get_quote(symbol: str) -> dict:
    """Function to get index quote

    Args:
        symbol (str): Symbol of the index

    Returns:
        dict: Dictionary containing the quote of the index
    """

    # Fetch and process the index
    return fetch_and_process_quote(symbol, filter=False)
