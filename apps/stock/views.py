# Imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from apps.socket.constants import BSE_CATEGORIES, NSE_CATEGORIES
from apps.socket.helpers import get_index_quotes
from apps.socket.utils import is_market_open
from apps.stock.forms import IndicesFilterForm


# Indices view
@login_required
def indices_view(request):
    """Indices view

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Create a form object
    form = IndicesFilterForm(request.GET)

    # Get the stock_exchange and category from the form data
    stock_exchange = form.data.get("stock_exchange", "NSE")
    category = form.data.get("category", "broad-market")

    # If invalid stock exchange
    if stock_exchange not in ["NSE", "BSE"]:
        # Set stock_exchange to NSE
        stock_exchange = "NSE"

        # Set the category to broad-market
        category = "broad-market"

        # Add an error message
        messages.error(request, "Invalid stock exchange selected!")

        # Redirect to the indices page
        return render(
            request,
            "stock/indices.html",
            {
                "user": request.user,
                "form": form,
                "stock_exchange": stock_exchange,
                "category": category,
                "category_name": "Broad Market",
                "quotes": get_index_quotes(stock_exchange, category),
                "is_market_open": is_market_open(),
            },
        )

    # If stock_exchange is NSE
    if stock_exchange == "NSE":
        # If invalid category
        if category not in dict(NSE_CATEGORIES).keys():
            # Set the category to broad-market
            category = "broad-market"

            # Add an error message
            messages.error(request, "Invalid category selected!")

            # Redirect to the indices page
            return render(
                request,
                "stock/indices.html",
                {
                    "user": request.user,
                    "form": form,
                    "stock_exchange": stock_exchange,
                    "category": category,
                    "category_name": "Broad Market",
                    "quotes": get_index_quotes(stock_exchange, category),
                    "is_market_open": is_market_open(),
                },
            )

    # If stock exchange is BSE
    else:
        # If invalid category
        if category not in dict(BSE_CATEGORIES).keys():
            # Set the category to broad-market
            category = "broad-market"

            # Add an error message
            messages.error(request, "Invalid category selected!")

            # Redirect to the indices page
            return render(
                request,
                "stock/indices.html",
                {
                    "user": request.user,
                    "form": form,
                    "stock_exchange": stock_exchange,
                    "category": category,
                    "category_name": "Broad Market",
                    "quotes": get_index_quotes(stock_exchange, category),
                    "is_market_open": is_market_open(),
                },
            )

    # Get the quotes for the indices
    quotes = get_index_quotes(stock_exchange, category)

    # If stock_exchange is NSE
    if stock_exchange == "NSE":
        # Get the category name
        category_name = dict(NSE_CATEGORIES).get(category, "Broad Market")

    # If stock_exchange is BSE
    else:
        # Get the category name
        category_name = dict(BSE_CATEGORIES).get(category, "Broad Market")

    # Context dictionary
    context = {
        "user": request.user,
        "form": form,
        "stock_exchange": stock_exchange,
        "category": category,
        "category_name": category_name,
        "quotes": quotes,
        "is_market_open": is_market_open(),
    }

    # Render the indices.html template
    return render(request, "stock/indices.html", context)


# Get categories view
@login_required
def get_categories_view(request):
    """Get categories view

    Args:
        request (HttpRequest): The request object

    Returns:
        JsonResponse: The response object
    """

    # Get the exchange
    exchange = request.GET.get("exchange")

    # Get the categories based on the exchange
    categories = NSE_CATEGORIES if exchange == "NSE" else BSE_CATEGORIES

    # Return the categories as a JSON response
    return JsonResponse({"categories": categories}, safe=False)
