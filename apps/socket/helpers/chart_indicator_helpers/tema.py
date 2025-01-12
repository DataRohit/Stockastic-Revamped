# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the Triple Exponential Moving Average (TEMA)
def add_tema_indicator(
    fig: go.Figure, history_df: pd.DataFrame, window: int = 20
) -> go.Figure:
    """Add the Triple Exponential Moving Average (TEMA) indicator to the given plot.

    TEMA is a smoother and faster-moving indicator compared to traditional EMA by
    reducing lag further.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The window size for the TEMA calculation. Defaults to 20.

    Returns:
        go.Figure: The plot with the TEMA indicator added.
    """

    # Calculate the first EMA
    ema1 = history_df["Close"].ewm(span=window, adjust=False).mean()

    # Calculate the second EMA from the first EMA
    ema2 = ema1.ewm(span=window, adjust=False).mean()

    # Calculate the third EMA from the second EMA
    ema3 = ema2.ewm(span=window, adjust=False).mean()

    # Calculate the TEMA
    history_df["TEMA"] = 3 * ema1 - 3 * ema2 + ema3

    # Add TEMA trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["TEMA"],
            mode="lines",
            line=dict(color="#8A2BE2", width=2),
            name=f"TEMA {window}",
        )
    )

    # Return the figure
    return fig
