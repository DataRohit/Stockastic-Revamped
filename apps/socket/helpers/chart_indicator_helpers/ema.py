# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the Expontential Moving Average (EMA)
def add_ema_indicator(
    fig: go.Figure, history_df: pd.DataFrame, window: int = 20
) -> go.Figure:
    """Add the Expontential Moving Average (EMA) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The window size for the EMA calculation. Defaults to 20.

    Returns:
        go.Figure: The plot with the EMA indicator added.
    """

    # Calculate the EMA
    history_df["EMA"] = history_df["Close"].ewm(span=window, adjust=False).mean()

    # Add EMA trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["EMA"],
            mode="lines",
            line=dict(color="#FF7F50", width=2),
            name=f"EMA {window}",
        )
    )

    # Return the figure
    return fig
