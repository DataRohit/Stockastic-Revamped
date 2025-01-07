# Imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.dashboard.models import StockIndexWatchlist
from apps.socket.constants import BSE_CATEGORIES, NSE_CATEGORIES
from apps.socket.helpers import (
    generate_candlestick_chart,
    get_index_quotes,
    get_quote,
    get_top_equity_gainers_20_quotes,
    get_top_equity_losers_20_quotes,
)
from apps.socket.utils import is_market_open
from apps.stock.forms import GainersLosersFilterForm, IndicesFilterForm


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


# Index quote view
@login_required
def index_quote_view(request, symbol: str):
    """Index quote view

    Args:
        request (HttpRequest): The request object
        symbol (str): The symbol of the index

    Returns:
        HttpResponse: The response object
    """

    # Get the index quote
    quote = get_quote(symbol)[-1]

    # Generate the candle stick chart
    chart = generate_candlestick_chart(symbol)

    # Check if the quote is bookmarked
    is_bookmarked = StockIndexWatchlist.objects.filter(
        user=request.user, symbol=symbol
    ).exists()

    # Create a context dictionary
    context = {
        "user": request.user,
        "symbol": symbol,
        "quote": quote,
        "is_bookmarked": is_bookmarked,
        "is_market_open": is_market_open(),
        "chart": chart.to_html(),
    }

    # Render the home.html template
    return render(request, "stock/index_quote.html", context)


# Top gainers view
@login_required
def equity_top_gainers_view(request):
    """Equity top gainers view

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Create a form object
    form = GainersLosersFilterForm(request.GET)

    # Get the stock_exchange and category from the form data
    stock_exchange = form.data.get("stock_exchange", "NSE")

    # If invalid stock exchange
    if stock_exchange not in ["NSE", "BSE"]:
        # Set stock_exchange to NSE
        stock_exchange = "NSE"

        # Add an error message
        messages.error(request, "Invalid stock exchange selected!")

    # Context dictionary
    context = {
        "user": request.user,
        "form": form,
        "gainers": get_top_equity_gainers_20_quotes(stock_exchange),
        "stock_exchange": stock_exchange,
        "is_market_open": is_market_open(),
    }

    # Render the top_gainers.html template
    return render(request, "stock/top_gainers.html", context)


# Top losers view
@login_required
def equity_top_losers_view(request):
    """Equity top losers view

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Create a form object
    form = GainersLosersFilterForm(request.GET)

    # Get the stock_exchange and category from the form data
    stock_exchange = form.data.get("stock_exchange", "NSE")

    # If invalid stock exchange
    if stock_exchange not in ["NSE", "BSE"]:
        # Set stock_exchange to NSE
        stock_exchange = "NSE"

        # Add an error message
        messages.error(request, "Invalid stock exchange selected!")

    # Context dictionary
    context = {
        "user": request.user,
        "form": form,
        "losers": get_top_equity_losers_20_quotes(stock_exchange),
        "stock_exchange": stock_exchange,
        "is_market_open": is_market_open(),
    }

    # Render the top_losers.html template
    return render(request, "stock/top_losers.html", context)


# Equity quote view
@login_required
def equity_quote_view(request, symbol: str):
    """Equity quote view

    Args:
        request (HttpRequest): The request object
        symbol (str): The symbol of the equity

    Returns:
        HttpResponse: The response object
    """

    # Get the equity quote
    quote = get_quote(symbol)[-1]

    # If the the symbol was invalid
    if quote is None or quote["quoteType"] != "EQUITY":
        # Add an error message
        messages.error(request, "Equity Stock Not Found!")

        # Redirect to explore page
        return redirect(reverse("core:explore"))

    # Generate the candle stick chart
    chart = generate_candlestick_chart(symbol)

    # Get the symbol from the quote
    symbol = quote["symbol"]

    # Extract the base symbol
    base_symbol = symbol.split(".")[0]

    # Create symbol for nse and bse
    nse_symbol = base_symbol + ".NS"
    bse_symbol = base_symbol + ".BO"

    # Check if the quote is bookmarked
    is_bookmarked = StockIndexWatchlist.objects.filter(
        user=request.user, symbol=symbol
    ).exists()

    # Create a context dictionary
    context = {
        "user": request.user,
        "symbol": symbol,
        "nse_symbol": nse_symbol,
        "bse_symbol": bse_symbol,
        "quote": quote,
        "is_bookmarked": is_bookmarked,
        "is_market_open": is_market_open(),
        "chart": chart.to_html(),
    }

    # Render the home.html template
    return render(request, "stock/equity_quote.html", context)


# Index Quote Bookmark View
@login_required
def index_quote_bookmark_view(request, symbol: str):
    """Index Quote Bookmark View

    Args:
        request (HttpRequest): The request object
        symbol (str): The symbol of the index

    Returns:
        HttpResponse: The response object
    """

    # Get the index quote
    quote = get_quote(symbol)[-1]

    # If the quote is not found
    if quote is None:
        # Add an error message
        messages.error(request, "Index Stock Not Found!")

        # Redirect to explore page
        return redirect(reverse("core:explore"))

    # Get the stock index watchlist
    _, created = StockIndexWatchlist.objects.get_or_create(
        user=request.user, symbol=symbol, type="INDEX"
    )

    # If the stock index watchlist was created
    if created:
        # Add a success message
        messages.success(request, f"{symbol} Added to Watchlist!")

    # If the stock index watchlist already exists
    else:
        # Add a warning message
        messages.warning(request, f"{symbol} Already in Watchlist!")

    # Redirect to the index quote page
    return redirect(reverse("stock:indexQuote", kwargs={"symbol": symbol}))


# Index Quote Unbookmark View
@login_required
def index_quote_unbookmark_view(request, symbol: str):
    """Index Quote Unbookmark View

    Args:
        request (HttpRequest): The request object
        symbol (str): The symbol of the index

    Returns:
        HttpResponse: The response object
    """

    # Get the stock index watchlist
    stock_index_watchlist = StockIndexWatchlist.objects.filter(
        user=request.user, symbol=symbol, type="INDEX"
    )

    # If the stock index watchlist exists
    if stock_index_watchlist.exists():
        # Delete the stock index watchlist
        stock_index_watchlist.delete()

        # Add a success message
        messages.success(request, f"{symbol} Removed from Watchlist!")

    # If the stock index watchlist does not exist
    else:
        # Add a warning message
        messages.warning(request, f"{symbol} Not in Watchlist!")

    # Redirect to the index quote page
    return redirect(reverse("stock:indexQuote", kwargs={"symbol": symbol}))


# Equity Bookmark View
@login_required
def equity_bookmark_view(request, symbol: str):
    """Equity Bookmark View

    Args:
        request (HttpRequest): The request object
        symbol (str): The symbol of the equity

    Returns:
        HttpResponse: The response object
    """

    # Get the equity quote
    quote = get_quote(symbol)[-1]

    # If the quote is not found
    if quote is None or quote["quoteType"] != "EQUITY":
        # Add an error message
        messages.error(request, "Equity Stock Not Found!")

        # Redirect to explore page
        return redirect(reverse("core:explore"))

    # Get the symbol from the quote
    symbol = quote["symbol"]

    # Extract the base symbol
    base_symbol = symbol.split(".")[0]

    # Create symbol for nse and bse
    nse_symbol = base_symbol + ".NS"
    bse_symbol = base_symbol + ".BO"

    # Get the stock equity watchlist
    _, created = StockIndexWatchlist.objects.get_or_create(
        user=request.user, symbol=nse_symbol, type="EQUITY"
    )

    # If the stock equity watchlist was created
    if created:
        # Add a success message
        messages.success(request, f"{nse_symbol} Added to Watchlist!")

    # If the stock equity watchlist already exists
    else:
        # Add a warning message
        messages.warning(request, f"{nse_symbol} Already in Watchlist!")

    # Get the stock equity watchlist
    _, created = StockIndexWatchlist.objects.get_or_create(
        user=request.user, symbol=bse_symbol, type="EQUITY"
    )

    # If the stock equity watchlist was created
    if created:
        # Add a success message
        messages.success(request, f"{bse_symbol} Added to Watchlist!")

    # If the stock equity watchlist already exists
    else:
        # Add a warning message
        messages.warning(request, f"{bse_symbol} Already in Watchlist!")

    # Redirect to the equity quote page
    return redirect(reverse("stock:equityQuote", kwargs={"symbol": symbol}))


# Equity Unbookmark View
@login_required
def equity_unbookmark_view(request, symbol: str):
    """Equity Unbookmark View

    Args:
        request (HttpRequest): The request object
        symbol (str): The symbol of the equity

    Returns:
        HttpResponse: The response object
    """

    # Extract the base symbol
    base_symbol = symbol.split(".")[0]

    # Create symbol for nse and bse
    nse_symbol = base_symbol + ".NS"
    bse_symbol = base_symbol + ".BO"

    # Get the stock equity watchlist
    stock_index_watchlist = StockIndexWatchlist.objects.filter(
        user=request.user, symbol=nse_symbol, type="EQUITY"
    )

    # If the stock equity watchlist exists
    if stock_index_watchlist.exists():
        # Delete the stock equity watchlist
        stock_index_watchlist.delete()

        # Add a success message
        messages.success(request, f"{nse_symbol} Removed from Watchlist!")

    # If the stock equity watchlist does not exist
    else:
        # Add a warning message
        messages.warning(request, f"{nse_symbol} Not in Watchlist!")

    # Get the stock equity watchlist
    stock_index_watchlist = StockIndexWatchlist.objects.filter(
        user=request.user, symbol=bse_symbol, type="EQUITY"
    )

    # If the stock equity watchlist exists
    if stock_index_watchlist.exists():
        # Delete the stock equity watchlist
        stock_index_watchlist.delete()

        # Add a success message
        messages.success(request, f"{bse_symbol} Removed from Watchlist!")

    # If the stock equity watchlist does not exist
    else:
        # Add a warning message
        messages.warning(request, f"{bse_symbol} Not in Watchlist!")

    # Redirect to the equity quote page
    return redirect(reverse("stock:equityQuote", kwargs={"symbol": symbol}))
