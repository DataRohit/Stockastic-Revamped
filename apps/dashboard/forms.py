# Imports
from django import forms

from apps.socket.constants import INDICATORS, INTERVALS, PERIODS


# Chart filter form
class ChartFilterForm(forms.Form):
    """Chart filter form

    Inherits:
        forms.Form

    Attributes:
        period (forms.ChoiceField): The period
        interval (forms.ChoiceField): The interval
    """

    # Attributes
    period = forms.ChoiceField(
        label="Period",
        choices=PERIODS,
        initial="1d",
        required=True,
        widget=forms.Select(),
    )
    interval = forms.ChoiceField(
        label="Interval",
        choices=INTERVALS["1d"],
        required=True,
        widget=forms.Select(),
    )
    indicator = forms.ChoiceField(
        label="Indicator",
        choices=INDICATORS,
        initial="none",
        required=True,
        widget=forms.Select(),
    )
