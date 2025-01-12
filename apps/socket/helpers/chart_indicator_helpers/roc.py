# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the ROC (Rate of Change) Indicator
def add_roc_indicator(
    fig: go.Figure, history_df: pd.DataFrame, period: int = 14
) -> go.Figure:
    """Add the Rate of Change (ROC) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        period (int, optional): The lookback period for calculating the ROC. Defaults to 14.

    Returns:
        go.Figure: The plot with the ROC indicator added.
    """

    # Calculate ROC
    history_df["ROC"] = (
        (history_df["Close"] - history_df["Close"].shift(period))
        / history_df["Close"].shift(period)
    ) * 100

    # Add ROC trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["ROC"],
            mode="lines",
            line=dict(color="#FFA500", width=2),
            name=f"ROC ({period})",
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
            title="Rate of Change (ROC)",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
