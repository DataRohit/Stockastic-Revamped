# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# StockConfig
class StockConfig(AppConfig):
    """StockConfig

    Inherits:
        AppConfig

    Attributes:
        default_auto_field (str): "django.db.models.BigAutoField"
        name (str): "apps.stock"
        verbose_name (str): _("Stock")
    """

    # Attributes
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.stock"
    verbose_name = _("Stock")
