# Imports
import datetime

from django.utils import timezone


# Function to check if market is open
def is_market_open():
    """Check if market is open

    Returns:
        bool: True if market is open, False otherwise
    """

    # Get the current time and week day in the local timezone
    current_datetime = timezone.localtime()
    current_time = current_datetime.time()
    current_weekday = current_datetime.weekday()

    # Check if the current day is a weekend (Saturday or Sunday)
    if current_weekday in [5, 6]:
        # Market is closed on weekends
        return False

    # Define the time range for market open (from 09:15 to 15:30)
    start_time = datetime.time(9, 15)
    end_time = datetime.time(15, 30)

    # Check if current_time is within the defined time range
    if start_time <= current_time <= end_time:
        # Market is open
        return True

    # Market is closed
    return False
