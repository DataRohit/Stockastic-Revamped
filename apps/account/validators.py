# Imports
from django.core import validators
from django.utils.translation import gettext_lazy as _


# Username Validator
class UsernameValidator(validators.RegexValidator):
    """Username Validator

    UsernameValidator class is used to validate the username field

    Inherits:
        RegexValidator

    Attributes:
        regex (str): The regular expression for the username field
        message (str): The error message for the username field
        flags (int): The flags for the regular expression
    """

    # Attributes
    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Your username is not valid. A username can only contain letters, numbers, a dot, @ symbol, + symbol and a hyphen"
    )
    flags = 0
