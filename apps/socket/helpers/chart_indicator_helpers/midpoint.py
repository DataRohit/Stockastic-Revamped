# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the MidPoint indicator
def add_midpoint_indicator(
    fig: go.Figure, history_df: pd.DataFrame, period: int = 14
) -> go.Figure:
    """Add the MidPoint indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        period (int, optional): The period over which to calculate the midpoint. Defaults to 14.

    Returns:
        go.Figure: The plot with the MidPoint indicator added.
    """

    # Calculate the MidPoint (highest high + lowest low) / 2 over the period
    history_df["MidPoint"] = (
        history_df["High"].rolling(window=period).max()
        + history_df["Low"].rolling(window=period).min()
    ) / 2

    # Add MidPoint trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["MidPoint"],
            mode="lines",
            line=dict(color="#FF8C00", width=2),
            name=f"MidPoint ({period})",
            yaxis="y2",
        )
    )

    # Update layout to add secondary Y-axis for MidPoint
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="MidPoint Indicator",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
