# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the Stochastic RSI (StochRSI) with dual Y-axis
def add_stochastic_rsi_indicator(
    fig: go.Figure, history_df: pd.DataFrame, window: int = 14, smooth_window: int = 3
) -> go.Figure:
    """Add the Stochastic RSI (StochRSI) indicator with a dual Y-axis to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The window size for calculating the RSI. Defaults to 14.
        smooth_window (int, optional): The window size for smoothing the StochRSI to get the signal line. Defaults to 3.

    Returns:
        go.Figure: The plot with the Stochastic RSI (StochRSI) indicator added and dual Y-axis.
    """

    # Calculate the RSI (Relative Strength Index)
    delta = history_df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    history_df["RSI"] = 100 - (100 / (1 + rs))

    # Calculate the Stochastic RSI
    lowest_rsi = history_df["RSI"].rolling(window).min()
    highest_rsi = history_df["RSI"].rolling(window).max()
    history_df["StochRSI"] = (history_df["RSI"] - lowest_rsi) / (
        highest_rsi - lowest_rsi
    )

    # Smooth the Stochastic RSI to get the signal line
    history_df["StochRSI_Smooth"] = history_df["StochRSI"].rolling(smooth_window).mean()

    # Add Stochastic RSI trace (using secondary y-axis)
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["StochRSI"],
            mode="lines",
            line=dict(color="#FF6347", width=2),
            name=f"StochRSI {window}",
            yaxis="y2",
        )
    )

    # Add the Stochastic RSI smoothed signal line (using secondary y-axis)
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["StochRSI_Smooth"],
            mode="lines",
            line=dict(color="#32CD32", width=2, dash="dot"),
            name=f"StochRSI Signal {smooth_window}",
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
            title="Stochastic RSI",
            overlaying="y",
            side="right",
            range=[0, 1],
        ),
    )

    # Return the figure
    return fig
