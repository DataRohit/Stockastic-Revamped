# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the Average True Range (ATR) indicator
def add_atr_indicator(
    fig: go.Figure, history_df: pd.DataFrame, period: int = 14
) -> go.Figure:
    """Add the Average True Range (ATR) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        period (int, optional): The period for calculating the ATR. Defaults to 14.

    Returns:
        go.Figure: The plot with the ATR indicator added.
    """

    # Calculate True Range (TR)
    history_df["TR"] = pd.concat(
        [
            history_df["High"] - history_df["Low"],
            abs(history_df["High"] - history_df["Close"].shift(1)),
            abs(history_df["Low"] - history_df["Close"].shift(1)),
        ],
        axis=1,
    ).max(axis=1)

    # Calculate ATR (Simple Moving Average of True Range)
    history_df["ATR"] = history_df["TR"].rolling(window=period).mean()

    # Add ATR trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["ATR"],
            mode="lines",
            line=dict(color="#00BFFF", width=2),
            name=f"ATR ({period})",
            yaxis="y2",
        )
    )

    # Update layout to add secondary Y-axis for ATR
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="ATR Indicator",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
