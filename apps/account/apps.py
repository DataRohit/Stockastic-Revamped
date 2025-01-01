# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# AccountConfig
class AccountConfig(AppConfig):
    """AccountConfig

    Inherits:
        AppConfig

    Attributes:
        default_auto_field (str): "django.db.models.BigAutoField"
        name (str): "apps.account"
        verbose_name (str): _("Account")
    """

    # Attributes
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.account"
    verbose_name = _("Account")
