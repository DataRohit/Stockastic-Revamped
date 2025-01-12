# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the Williams %R (WillR) Indicator
def add_williams_r_indicator(
    fig: go.Figure, history_df: pd.DataFrame, window: int = 14
) -> go.Figure:
    """Add the Williams %R (WillR) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The window size for the WillR calculation. Defaults to 14.

    Returns:
        go.Figure: The plot with the Williams %R (WillR) indicator added.
    """

    # Calculate the highest high and lowest low over the window period
    highest_high = history_df["High"].rolling(window).max()
    lowest_low = history_df["Low"].rolling(window).min()

    # Calculate Williams %R (WillR)
    history_df["WillR"] = (
        -100 * (highest_high - history_df["Close"]) / (highest_high - lowest_low)
    )

    # Add Williams %R trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["WillR"],
            mode="lines",
            line=dict(color="#1F77B4", width=2),
            name=f"WillR {window}",
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
            title="Williams %R",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
