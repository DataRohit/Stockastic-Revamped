# Imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.dashboard.forms import ChartFilterForm
from apps.dashboard.models import StockIndexWatchlist
from apps.socket.constants import INTERVALS, PERIODS
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


# Get Period Intervals View
def get_period_intervals_view(request):
    """Get Period Intervals View

    Args:
        request (HttpRequest): The request object

    Returns:
        JsonResponse: The response object
    """

    # Get the period from query parameters
    period = request.GET.get("period", "1d")

    # Return the intervals as a JSON response
    return JsonResponse({"intervals": INTERVALS[period]})


# Playground View
@login_required
def playground_view(request, symbol: str):
    """Playground View

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Initialize the form
    form = ChartFilterForm(request.GET)

    # Get the period and interval
    period = form.data.get("period", "1d")
    interval = form.data.get("interval", "5m")
    indicator = form.data.get("indicator", "none")

    # Check if period and interval are valid
    if period not in dict(PERIODS) or interval not in dict(INTERVALS[period]):
        # Add a flash message
        messages.error(request, "Invalid period or interval")

        # Redirect to the dashboard
        return redirect(reverse("core:explore"))

    # Get the intervals for the period
    intervals = INTERVALS[period]

    # Set the initial interval
    form.fields["interval"].initial = interval

    # Set the choices for the interval field
    form.fields["interval"].choices = intervals

    # Set the initial indicator
    form.fields["indicator"].initial = indicator

    # Get the quote for the symbol
    quote = get_quote(symbol)

    # If the quote is None
    if quote is None:
        # Add a flash message
        messages.error(request, f"Invalid symbol: {symbol}")

        # Redirect to the dashboard
        return redirect(reverse("core:explore"))

    # Generate the candlestick chart
    chart = generate_candlestick_chart(symbol, period, interval, indicator, 800)

    # Create a context dictionary
    context = {
        "user": request.user,
        "form": form,
        "quote": quote[1],
        "chart": chart.to_html(),
    }

    # Render the playground.html template
    return render(request, "dashboard/playground.html", context)
