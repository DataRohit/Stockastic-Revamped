# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the True Range (TRANGE) indicator
def add_trange_indicator(fig: go.Figure, history_df: pd.DataFrame) -> go.Figure:
    """Add the True Range (TRANGE) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.

    Returns:
        go.Figure: The plot with the True Range (TRANGE) indicator added.
    """

    # Calculate the True Range (TRANGE)
    history_df["TrueRange"] = pd.concat(
        [
            history_df["High"] - history_df["Low"],
            abs(history_df["High"] - history_df["Close"].shift(1)),
            abs(history_df["Low"] - history_df["Close"].shift(1)),
        ],
        axis=1,
    ).max(axis=1)

    # Add TRANGE trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["TrueRange"],
            mode="lines",
            line=dict(color="#FFD700", width=2),
            name="True Range",
            yaxis="y2",
        )
    )

    # Update layout to add secondary Y-axis for True Range
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="True Range Indicator",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
