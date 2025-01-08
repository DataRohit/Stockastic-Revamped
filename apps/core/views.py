# Imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.socket.helpers import (
    get_top_equity_gainers_quotes,
    get_top_equity_losers_quotes,
    get_top_index_quotes,
)
from apps.socket.utils import is_market_open


# Home view
def home_view(request):
    """Home view

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # If user is authenticated
    if request.user.is_authenticated:
        # Redirect to explore view
        return redirect(reverse("core:explore"))

    # Create a context dictionary
    context = {"user": request.user}

    # Render the home.html template
    return render(request, "core/home.html", context)


# Explore view
@login_required
def explore_view(request):
    """Explore view

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Create a context dictionary
    context = {
        "user": request.user,
        "indices": get_top_index_quotes(),
        "gainers": get_top_equity_gainers_quotes(),
        "losers": get_top_equity_losers_quotes(),
        "is_market_open": is_market_open(),
    }

    # Render the explore.html template
    return render(request, "core/explore.html", context)
