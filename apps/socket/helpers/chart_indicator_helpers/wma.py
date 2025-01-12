# Imports
import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the Weighted Moving Average (WMA)
def add_wma_indicator(
    fig: go.Figure, history_df: pd.DataFrame, window: int = 20
) -> go.Figure:
    """Add the Weighted Moving Average (WMA) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The window size for the WMA calculation. Defaults to 20.

    Returns:
        go.Figure: The plot with the WMA indicator added.
    """

    # Calculate WMA based on the 'Close' prices
    weights = list(range(1, window + 1))

    # Add WMA trace to the plot
    history_df["WMA"] = (
        history_df["Close"]
        .rolling(window)
        .apply(lambda prices: np.dot(prices, weights) / sum(weights), raw=True)
    )

    # Add WMA trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["WMA"],
            mode="lines",
            line=dict(color="#FFD700", width=2),
            name=f"WMA {window}",
        )
    )

    # Return the figure
    return fig
