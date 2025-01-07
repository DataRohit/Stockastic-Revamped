# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# DashboardConfig
class DashboardConfig(AppConfig):
    """DashboardConfig

    Inherits:
        AppConfig

    Attributes:
        default_auto_field (str): "django.db.models.BigAutoField"
        name (str): "apps.dashboard"
        verbose_name (str): _("Dashboard")
    """

    # Attributes
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dashboard"
    verbose_name = _("Dashboard")
