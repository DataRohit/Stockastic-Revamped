# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the Triangular Moving Average (TRIMA)
def add_trima_indicator(
    fig: go.Figure, history_df: pd.DataFrame, window: int = 20
) -> go.Figure:
    """Add the Triangular Moving Average (TRIMA) indicator to the given plot.

    TRIMA smooths price data by applying a double smoothing process, making it less sensitive to market noise.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The window size for the TRIMA calculation. Defaults to 20.

    Returns:
        go.Figure: The plot with the TRIMA indicator added.
    """

    # Calculate the simple moving average (SMA) of the simple moving average to get TRIMA
    sma1 = history_df["Close"].rolling(window=window).mean()
    trima = sma1.rolling(window=window).mean()

    # Store TRIMA in the DataFrame
    history_df["TRIMA"] = trima

    # Add TRIMA trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["TRIMA"],
            mode="lines",
            line=dict(color="#FF6347", width=2),
            name=f"TRIMA {window}",
        )
    )

    # Return the figure
    return fig
