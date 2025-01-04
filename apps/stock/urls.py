# Imports
from django.urls import path

from apps.stock import views as stock_views

# Set the app name
app_name = "stock"

# URL patterns
urlpatterns = [
    path("indices/", stock_views.indices_view, name="indices"),
    path("indices/<str:symbol>/", stock_views.index_quote_view, name="indexQuote"),
    path(
        "api/indices/getCategories/",
        stock_views.get_categories_view,
        name="indicesGetCategories",
    ),
    path(
        "equity/topGainers/",
        stock_views.equity_top_gainers_view,
        name="equityTopGainers",
    ),
    path(
        "equity/topLosers/", stock_views.equity_top_losers_view, name="equityTopLosers"
    ),
    path("equity/<str:symbol>/", stock_views.equity_quote_view, name="equityQuote"),
]
