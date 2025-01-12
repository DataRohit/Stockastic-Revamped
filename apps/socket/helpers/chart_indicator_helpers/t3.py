# Imports
import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the T3 indicator (Triple Exponential Moving Average)
def add_t3_indicator(
    fig: go.Figure,
    history_df: pd.DataFrame,
    window: int = 10,
    vfactor: float = 0.7,
) -> go.Figure:
    """Add the T3 (Triple Exponential Moving Average) indicator to the given plot.

    The T3 indicator smooths the price data three times using an exponential moving average, with an additional volume factor to control smoothness.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The window size for calculating the moving average. Defaults to 10.
        vfactor (float, optional): The volume factor that influences the degree of smoothing. Defaults to 0.7.

    Returns:
        go.Figure: The plot with the T3 indicator added.
    """

    # Calculate the Exponential Moving Average (EMA) of the close prices
    def ema(series, window):
        """Calculate the Exponential Moving Average (EMA)."""
        return series.ewm(span=window, adjust=False).mean()

    # Calculate the first EMA (e1)
    e1 = ema(history_df["Close"], window)

    # Calculate the second EMA (e2) of e1
    e2 = ema(e1, window)

    # Calculate the third EMA (e3) of e2
    e3 = ema(e2, window)

    # Calculate the T3 as a weighted combination of e1, e2, and e3
    t3 = (1 + vfactor) * e1 - vfactor * e2

    # Apply EMA again to the T3 to get smoother results (apply it to the combination, not individual EMAs)
    t3 = ema(t3, window)

    # Add T3 trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=t3,
            mode="lines",
            line=dict(color="#FF6347", width=2),
            name=f"T3 {window}",
        )
    )

    # Return the figure
    return fig
