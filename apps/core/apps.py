# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# CoreConfig
class CoreConfig(AppConfig):
    """CoreConfig

    Inherits:
        AppConfig

    Attributes:
        default_auto_field (str): "django.db.models.BigAutoField"
        name (str): "apps.core"
        verbose_name (str): _("Core")
    """

    # Attributes
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = _("Core")
