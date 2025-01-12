# Imports
import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the MAMA indicator (Mature Adaptive Moving Average)
def add_mama_indicator(
    fig: go.Figure,
    history_df: pd.DataFrame,
    window: int = 10,
    fast_limit: float = 0.5,
    slow_limit: float = 0.05,
) -> go.Figure:
    """Add the MAMA (Mature Adaptive Moving Average) indicator to the given plot.

    The MAMA indicator adjusts to the market's volatility and trends, providing a smoother moving average.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The window size for calculating the moving averages. Defaults to 10.
        fast_limit (float, optional): The fast limit constant. Defaults to 0.5.
        slow_limit (float, optional): The slow limit constant. Defaults to 0.05.

    Returns:
        go.Figure: The plot with the MAMA indicator added.
    """

    # Calculate the price change
    price_change = history_df["Close"].diff()

    # Calculate the absolute value of price changes
    abs_price_change = abs(price_change)

    # Calculate the smoothing constants for FAMA and MAMA
    smoothing_constant = (
        abs_price_change / abs_price_change.rolling(window=window).sum()
    ) * (fast_limit - slow_limit) + slow_limit

    # Initialize MAMA and FAMA arrays
    fama = np.full_like(history_df["Close"], np.nan)
    mama = np.full_like(history_df["Close"], np.nan)

    # First values of FAMA and MAMA will be the same as the first closing price
    fama[window] = history_df["Close"].iloc[window]
    mama[window] = history_df["Close"].iloc[window]

    # Apply MAMA and FAMA calculations
    for i in range(window + 1, len(history_df)):
        # Calculate FAMA and MAMA based on the smoothing constant
        fama[i] = fama[i - 1] + smoothing_constant[i] * (
            history_df["Close"].iloc[i] - fama[i - 1]
        )
        mama[i] = mama[i - 1] + (1 - smoothing_constant[i]) * (
            history_df["Close"].iloc[i] - mama[i - 1]
        )

    # Store MAMA and FAMA in the DataFrame and drop initial NaN values
    mama_series = pd.Series(mama, index=history_df.index)
    fama_series = pd.Series(fama, index=history_df.index)

    # Forward fill missing values (bfill can be used depending on the use case)
    mama_series = mama_series.ffill()
    fama_series = fama_series.ffill()

    # Add MAMA and FAMA traces to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=mama_series,
            mode="lines",
            line=dict(color="#8A2BE2", width=2),
            name=f"MAMA {window}",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=fama_series,
            mode="lines",
            line=dict(color="#7FFF00", width=2),
            name=f"FAMA {window}",
        )
    )

    # Return the figure
    return fig
