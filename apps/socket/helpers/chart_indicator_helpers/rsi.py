# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the Relative Strength Index (RSI)
def add_rsi_indicator(
    fig: go.Figure, history_df: pd.DataFrame, window: int = 14
) -> go.Figure:
    """Add the Relative Strength Index (RSI) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The window size for the RSI calculation. Defaults to 14.

    Returns:
        go.Figure: The plot with the RSI indicator added.
    """

    # Calculate price changes
    delta = history_df["Close"].diff()

    # Calculate gains (positive price changes) and losses (negative price changes)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Calculate the rolling averages of gains and losses
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()

    # Calculate the Relative Strength (RS)
    rs = avg_gain / avg_loss

    # Calculate the RSI
    history_df["RSI"] = 100 - (100 / (1 + rs))

    # Add RSI trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["RSI"],
            mode="lines",
            line=dict(color="#FF6347", width=2),
            name=f"RSI {window}",
        )
    )

    # Return the figure
    return fig
