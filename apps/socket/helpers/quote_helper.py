# Imports
from concurrent.futures import ThreadPoolExecutor

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


# Function to get bookmarked quotes
def get_bookmarked_quotes(symbols: list) -> dict:
    """Function to get bookmarked quotes in parallel.

    Args:
        symbols (list): List of symbols.

    Returns:
        dict: Dictionary containing the quotes of the symbols.
    """

    # Dict to store the quotes
    quotes = {}

    # Use ThreadPoolExecutor to fetch quotes in parallel
    with ThreadPoolExecutor() as executor:
        results = executor.map(get_quote, symbols)

    # Convert results to dictionary
    quotes = dict(results)

    # Return the quotes
    return quotes
