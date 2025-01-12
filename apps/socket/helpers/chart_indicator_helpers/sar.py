# Imports
import pandas as pd
import plotly.graph_objects as go
from ta.trend import PSARIndicator


# Function to calculate and add the SAR indicator
def add_sar_indicator(
    fig: go.Figure, history_df: pd.DataFrame, step: float = 0.02, max_step: float = 0.2
) -> go.Figure:
    """Add the SAR (Parabolic Stop and Reverse) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        step (float, optional): The step increment for the SAR calculation. Defaults to 0.02.
        max_step (float, optional): The maximum step increment for the SAR calculation. Defaults to 0.2.

    Returns:
        go.Figure: The plot with the SAR indicator added.
    """

    # Calculate the SAR values using ta library
    psar = PSARIndicator(
        high=history_df["High"],
        low=history_df["Low"],
        close=history_df["Close"],
        step=step,
        max_step=max_step,
    )

    # Add the SAR trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=psar.psar(),
            mode="lines",
            marker=dict(color="#6A80B9", size=6, symbol="circle"),
            name="SAR Indicator",
            yaxis="y2",
        )
    )

    # Update layout to add secondary Y-axis for SAR
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="SAR (Stop and Reverse)",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
