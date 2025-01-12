# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the MidPrice indicator
def add_midprice_indicator(
    fig: go.Figure, history_df: pd.DataFrame, period: int = 14
) -> go.Figure:
    """Add the MidPrice indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        period (int, optional): The period over which to calculate the mid price. Defaults to 14.

    Returns:
        go.Figure: The plot with the MidPrice indicator added.
    """

    # Calculate the MidPrice (average of highest high and lowest low over the period)
    history_df["MidPrice"] = (
        history_df["High"].rolling(window=period).max()
        + history_df["Low"].rolling(window=period).min()
    ) / 2

    # Add MidPrice trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["MidPrice"],
            mode="lines",
            line=dict(color="#FFA500", width=2),
            name=f"MidPrice ({period})",
            yaxis="y2",
        )
    )

    # Update layout to add secondary Y-axis for MidPrice
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="MidPrice Indicator",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
