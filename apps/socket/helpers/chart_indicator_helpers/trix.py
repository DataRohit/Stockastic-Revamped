# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the TRIX (Triple Exponential Moving Average) indicator
def add_trix_indicator(
    fig: go.Figure, history_df: pd.DataFrame, period: int = 14, signal_period: int = 9
) -> go.Figure:
    """Add the TRIX (Triple Exponential Moving Average) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        period (int, optional): The lookback period for calculating the TRIX. Defaults to 14.
        signal_period (int, optional): The period for the signal line (smoothed TRIX). Defaults to 9.

    Returns:
        go.Figure: The plot with the TRIX indicator added.
    """

    # Calculate the first EMA
    history_df["EMA1"] = history_df["Close"].ewm(span=period, adjust=False).mean()

    # Calculate the second EMA (of EMA1)
    history_df["EMA2"] = history_df["EMA1"].ewm(span=period, adjust=False).mean()

    # Calculate the third EMA (of EMA2)
    history_df["EMA3"] = history_df["EMA2"].ewm(span=period, adjust=False).mean()

    # Calculate the TRIX line as the percentage rate of change of EMA3
    history_df["TRIX"] = history_df["EMA3"].pct_change() * 100

    # Calculate the signal line (smoothed TRIX)
    history_df["Signal"] = (
        history_df["TRIX"].ewm(span=signal_period, adjust=False).mean()
    )

    # Add TRIX trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["TRIX"],
            mode="lines",
            line=dict(color="#1E90FF", width=2),
            name=f"TRIX ({period})",
            yaxis="y2",
        )
    )

    # Add Signal line trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["Signal"],
            mode="lines",
            line=dict(color="#FF6347", width=2, dash="dash"),
            name=f"Signal ({signal_period})",
            yaxis="y2",
        )
    )

    # Update layout to add secondary Y-axis for TRIX and Signal
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="TRIX",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
