# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the Stochastic Fast (%K) Indicator (StochF)
def add_stochastic_fast_indicator(
    fig: go.Figure, history_df: pd.DataFrame, window: int = 14, smooth_window: int = 3
) -> go.Figure:
    """Add the Stochastic Fast (%K) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The window size for calculating the %K. Defaults to 14.
        smooth_window (int, optional): The window size for smoothing the %K to get the %D. Defaults to 3.

    Returns:
        go.Figure: The plot with the Stochastic Fast (%K) indicator added.
    """

    # Calculate the %K (Stochastic Fast)
    history_df["lowest_low"] = history_df["Low"].rolling(window).min()
    history_df["highest_high"] = history_df["High"].rolling(window).max()
    history_df["%K"] = (
        100
        * (history_df["Close"] - history_df["lowest_low"])
        / (history_df["highest_high"] - history_df["lowest_low"])
    )

    # Add the %K trace to the plot (Stochastic Fast)
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["%K"],
            mode="lines",
            line=dict(color="#1f77b4", width=2),
            name=f"%K {window}",
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
            title="Stochastic Fast (%K)",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
