# Imports
from django.contrib import admin

from apps.dashboard.models import StockIndexWatchlist


# Register the StockIndexWatchlist model
@admin.register(StockIndexWatchlist)
class StockIndexWatchlist(admin.ModelAdmin):
    """Admin class for the StockIndexWatchlist model.

    Inherits:
        admin.ModelAdmin

    Attributes:
        list_display: List of fields to display in the admin
        list_display_links: List of fields to link to the detail page
        list_filter: List of fields to filter the admin
        search_fields: List of fields to search the admin
        ordering: List of fields to order the admin
        readonly_fields: List of fields to display as read-only
        autocomplete_fields: List of fields to display as autocomplete
    """

    # Attributes
    list_display = ("id", "user", "symbol", "type")
    list_display_links = ("id", "user")
    list_filter = ("user", "symbol", "type")
    search_fields = ("user__username", "symbol")
    ordering = ("user", "symbol", "type")
    autocomplete_fields = ("user",)
    readonly_fields = ("type",)
