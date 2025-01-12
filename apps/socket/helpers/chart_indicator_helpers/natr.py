# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate and add the NATR indicator
def add_natr_indicator(
    fig: go.Figure, history_df: pd.DataFrame, period: int = 14
) -> go.Figure:
    """Add the Normalized Average True Range (NATR) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        period (int, optional): The period for calculating the NATR. Defaults to 14.

    Returns:
        go.Figure: The plot with the NATR indicator added.
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

    # Calculate NATR as (ATR / Close) * 100
    history_df["NATR"] = (history_df["ATR"] / history_df["Close"]) * 100

    # Add NATR trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["NATR"],
            mode="lines",
            line=dict(color="#DAA520", width=2),
            name=f"NATR ({period})",
            yaxis="y2",
        )
    )

    # Update layout to add secondary Y-axis for NATR
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="NATR Indicator",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
