# Imports
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

# Get the user model
User = get_user_model()


# StockIndexWatchlist model
class StockIndexWatchlist(models.Model):
    """Model definition for StockIndexWatchlist.

    Inherits:
        models.Model

    Attributes:
        pkid: Primary key for the model
        id: UUIDField for the unique identifier
        user: ForeignKey to User model
        symbol: CharField for the symbol name

    Meta:
        verbose_name: Singular name for the model
        verbose_name_plural: Plural name for the model

    Methods:
        __str__: Returns the string representation of the model
    """

    # Attributes
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="stock_index_watchlists"
    )
    symbol = models.CharField(_("Symbol"), max_length=255)

    # Meta
    class Meta:
        # Attributes
        verbose_name = _("StockIndex Watchlist")
        verbose_name_plural = _("StockIndex Watchlists")

    # String representation
    def __str__(self) -> str:
        # Return the string representation
        return f"{self.user} - {self.symbol}"
