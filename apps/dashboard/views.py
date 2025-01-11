# Imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.dashboard.models import StockIndexWatchlist
from apps.socket.helpers import generate_candlestick_chart, get_quote
from apps.socket.utils import is_market_open


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
        "is_market_open": is_market_open(),
        "quotes": quotes,
    }

    # Render the dashboard.html template
    return render(request, "dashboard/dashboard.html", context)


# Playground View
@login_required
def playground_view(request, symbol: str):
    """Playground View

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Get the quote for the symbol
    quote = get_quote(symbol)

    # If the quote is None
    if quote is None:
        # Add a flash message
        messages.error(request, f"Invalid symbol: {symbol}")

        # Redirect to the dashboard
        return redirect(reverse("core:explore"))

    # Generate the candlestick chart
    chart = generate_candlestick_chart(symbol)

    # Create a context dictionary
    context = {
        "user": request.user,
        "quote": quote[1],
        "chart": chart.to_html(),
    }

    # Render the playground.html template
    return render(request, "dashboard/playground.html", context)
