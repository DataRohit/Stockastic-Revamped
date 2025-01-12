# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the BOP (Balance of Power) Indicator
def add_bop_indicator(fig: go.Figure, history_df: pd.DataFrame) -> go.Figure:
    """Add the Balance of Power (BOP) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.

    Returns:
        go.Figure: The plot with the BOP indicator added.
    """

    # Calculate the BOP indicator
    history_df["BOP"] = (history_df["Close"] - history_df["Open"]) / (
        history_df["High"] - history_df["Low"]
    )

    # Handle division by zero in BOP calculation
    history_df["BOP"].replace([float("inf"), -float("inf")], 0, inplace=True)
    history_df["BOP"].fillna(0, inplace=True)

    # Add BOP trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["BOP"],
            mode="lines",
            line=dict(color="#FFA500", width=2),
            name="Balance of Power (BOP)",
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
            title="Balance of Power (BOP)",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
