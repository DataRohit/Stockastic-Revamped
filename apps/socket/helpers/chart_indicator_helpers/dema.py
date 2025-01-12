# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the Double Exponential Moving Average (DEMA)
def add_dema_indicator(
    fig: go.Figure, history_df: pd.DataFrame, window: int = 20
) -> go.Figure:
    """Add the Double Exponential Moving Average (DEMA) indicator to the given plot.

    DEMA is a smoother moving average compared to the traditional EMA by reducing lag.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The window size for the DEMA calculation. Defaults to 20.

    Returns:
        go.Figure: The plot with the DEMA indicator added.
    """

    # Calculate the first EMA
    ema1 = history_df["Close"].ewm(span=window, adjust=False).mean()

    # Calculate the second EMA on the previously calculated EMA
    ema2 = ema1.ewm(span=window, adjust=False).mean()

    # Calculate the DEMA
    history_df["DEMA"] = 2 * ema1 - ema2

    # Add DEMA trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["DEMA"],
            mode="lines",
            line=dict(color="#00BFFF", width=2),
            name=f"DEMA {window}",
        )
    )

    # Return the figure
    return fig
