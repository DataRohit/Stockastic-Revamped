# Imports
from django import forms

from apps.socket.constants import NSE_CATEGORIES


# Indices filter form
class IndicesFilterForm(forms.Form):
    """Indices filter form

    Inherits:
        forms.Form

    Attributes:
        stock_exchange (forms.ChoiceField): The stock exchange
        category (forms.ChoiceField): The category
    """

    # Attributes
    stock_exchange = forms.ChoiceField(
        label="Stock Exchange",
        choices=[("NSE", "NSE"), ("BSE", "BSE")],
        initial="NSE",
        required=True,
        widget=forms.Select(),
    )
    category = forms.ChoiceField(
        label="Category",
        choices=NSE_CATEGORIES,
        required=True,
        widget=forms.Select(),
    )


# GainersLosers filter form
class GainersLosersFilterForm(forms.Form):
    """GainersLosers filter form

    Inherits:
        forms.Form

    Attributes:
        stock_exchange (forms.ChoiceField): The stock exchange
    """

    # Attributes
    stock_exchange = forms.ChoiceField(
        label="Stock Exchange",
        choices=[("NSE", "NSE"), ("BSE", "BSE")],
        initial="NSE",
        required=True,
        widget=forms.Select(),
    )
