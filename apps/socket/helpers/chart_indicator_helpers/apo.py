# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the APO (Absolute Price Oscillator) Indicator
def add_apo_indicator(
    fig: go.Figure,
    history_df: pd.DataFrame,
    fast_period: int = 12,
    slow_period: int = 26,
) -> go.Figure:
    """Add the Absolute Price Oscillator (APO) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        fast_period (int, optional): The period for the fast EMA. Defaults to 12.
        slow_period (int, optional): The period for the slow EMA. Defaults to 26.

    Returns:
        go.Figure: The plot with the APO indicator added.
    """

    # Calculate the fast and slow EMAs
    history_df["EMA_Fast"] = (
        history_df["Close"].ewm(span=fast_period, adjust=False).mean()
    )
    history_df["EMA_Slow"] = (
        history_df["Close"].ewm(span=slow_period, adjust=False).mean()
    )

    # Calculate the APO
    history_df["APO"] = history_df["EMA_Fast"] - history_df["EMA_Slow"]

    # Add APO trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["APO"],
            mode="lines",
            line=dict(color="#FFA500", width=2),
            name=f"APO ({fast_period}, {slow_period})",
            yaxis="y2",
        )
    )

    # Update layout for visibility
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="APO",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
