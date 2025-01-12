# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the MACD indicator
def add_macd_indicator(
    fig: go.Figure,
    history_df: pd.DataFrame,
    short_window: int = 12,
    long_window: int = 26,
    signal_window: int = 9,
) -> go.Figure:
    """Add the MACD (Moving Average Convergence Divergence) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        short_window (int, optional): The short window size for the MACD calculation. Defaults to 12.
        long_window (int, optional): The long window size for the MACD calculation. Defaults to 26.
        signal_window (int, optional): The window size for the signal line calculation. Defaults to 9.

    Returns:
        go.Figure: The plot with the MACD indicator added.
    """

    # Calculate the short-term and long-term EMA
    history_df["EMA_short"] = (
        history_df["Close"].ewm(span=short_window, adjust=False).mean()
    )
    history_df["EMA_long"] = (
        history_df["Close"].ewm(span=long_window, adjust=False).mean()
    )

    # Calculate MACD line
    history_df["MACD"] = history_df["EMA_short"] - history_df["EMA_long"]

    # Calculate Signal line
    history_df["Signal"] = (
        history_df["MACD"].ewm(span=signal_window, adjust=False).mean()
    )

    # Add MACD trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["MACD"],
            mode="lines",
            line=dict(color="blue", width=2),
            name="MACD",
            yaxis="y2",
        )
    )

    # Add Signal line trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["Signal"],
            mode="lines",
            line=dict(color="orange", width=2),
            name="Signal",
            yaxis="y2",
        )
    )

    # Update layout to add secondary Y-axis
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="MACD",
            overlaying="y",
            side="right",
            range=[history_df["MACD"].min(), history_df["MACD"].max()],
        ),
    )

    # Return the figure
    return fig
