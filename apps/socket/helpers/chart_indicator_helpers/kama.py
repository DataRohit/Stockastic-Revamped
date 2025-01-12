# Imports
import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Refined KAMA Function with fixes for deprecation warnings and visibility issue
def add_kama_indicator(
    fig: go.Figure,
    history_df: pd.DataFrame,
    window: int = 10,
    fast: int = 2,
    slow: int = 30,
) -> go.Figure:
    """Add the Kaufman's Adaptive Moving Average (KAMA) indicator to the given plot.

    KAMA adapts to market conditions by considering both price volatility and trends.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The efficiency ratio period. Defaults to 10.
        fast (int, optional): The fastest smoothing constant period. Defaults to 2.
        slow (int, optional): The slowest smoothing constant period. Defaults to 30.

    Returns:
        go.Figure: The plot with the KAMA indicator added.
    """

    # Calculate price changes over the window period
    change = abs(history_df["Close"].diff(window))

    # Calculate the efficiency ratio (ER)
    volatility = abs(history_df["Close"].diff()).rolling(window=window).sum()
    er = np.divide(change, volatility, out=np.zeros_like(change), where=volatility != 0)

    # Calculate smoothing constants
    fast_sc = 2 / (fast + 1)
    slow_sc = 2 / (slow + 1)
    smoothing_constant = (er * (fast_sc - slow_sc) + slow_sc) ** 2

    # Initialize KAMA series with NaNs
    kama = np.full_like(history_df["Close"], np.nan)

    # Initialize first KAMA value to be the first closing price after the window
    kama[window] = history_df["Close"].iloc[window]

    # Apply KAMA calculation iteratively
    for i in range(window + 1, len(history_df)):
        kama[i] = kama[i - 1] + smoothing_constant[i] * (
            history_df["Close"].iloc[i] - kama[i - 1]
        )

    # Store KAMA in the DataFrame and drop initial NaN values
    kama_series = pd.Series(kama, index=history_df.index)

    # Forward fill missing values (bfill can be used depending on the use case)
    kama_series = kama_series.ffill()

    # Add KAMA trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=kama_series,
            mode="lines",
            line=dict(color="#4B0082", width=2),
            name=f"KAMA {window}",
        )
    )

    # Return the figure
    return fig
