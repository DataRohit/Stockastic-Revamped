# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# SocketConfig
class SocketConfig(AppConfig):
    """SocketConfig

    Inherits:
        AppConfig

    Attributes:
        default_auto_field (str): "django.db.models.BigAutoField"
        name (str): "apps.socket"
        verbose_name (str): _("Socket")
    """

    # Attributes
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.socket"
    verbose_name = _("Socket")
