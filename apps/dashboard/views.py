# Imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.dashboard.models import StockIndexWatchlist
from apps.socket.helpers import get_quote


# Dashboard Home View
@login_required
def home_view(request):
    """Dashboard Home View

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Fetch the bookmarked indices and stocks
    bookmarked_items = StockIndexWatchlist.objects.filter(user=request.user).order_by(
        "-type", "symbol"
    )

    # Dict to store the quotes
    quotes = {}

    # Traverse over the bookmarked items
    for item in bookmarked_items:
        # Get the quote for the item
        quote = get_quote(item.symbol)

        # Append the quote to the quotes dict
        quotes[quote[0]] = quote[1]

    # Create a context dictionary
    context = {
        "user": request.user,
        "quotes": quotes,
    }

    # Render the dashboard.html template
    return render(request, "dashboard/dashboard.html", context)
