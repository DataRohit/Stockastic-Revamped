# Imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.socket.helpers import get_top_index_quotes
from apps.socket.utils import is_market_open


# Home view
def home_view(request):
    """Home view

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Create a context dictionary
    context = {"user": request.user}

    # Render the home.html template
    return render(request, "core/home.html", context)


# Dashboard view
@login_required
def dashboard_view(request):
    """Dashboard view

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Get the top index quotes
    top_index_quotes = get_top_index_quotes()

    # Create a context dictionary
    context = {
        "user": request.user,
        "quotes": top_index_quotes,
        "is_market_open": is_market_open(),
    }

    # Render the dashboard.html template
    return render(request, "core/dashboard.html", context)
