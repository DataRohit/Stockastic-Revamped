# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the Simple Moving Average (SMA)
def add_sma_indicator(
    fig: go.Figure, history_df: pd.DataFrame, window: int = 20
) -> go.Figure:
    """Add the Simple Moving Average (SMA) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The window size for the SMA calculation. Defaults to 20.

    Returns:
        go.Figure: The plot with the SMA indicator added.
    """

    # Calculate the SMA
    history_df["SMA"] = history_df["Close"].rolling(window=window).mean()

    # Add SMA trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["SMA"],
            mode="lines",
            line=dict(color="#FFA500", width=2),
            name=f"SMA {window}",
        )
    )

    # Return the figure
    return fig
