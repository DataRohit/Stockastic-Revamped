# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the ROCR (Rate of Change Ratio) Indicator
def add_rocr_indicator(
    fig: go.Figure, history_df: pd.DataFrame, period: int = 14
) -> go.Figure:
    """Add the Rate of Change Ratio (ROCR) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        period (int, optional): The lookback period for calculating the ROCR. Defaults to 14.

    Returns:
        go.Figure: The plot with the ROCR indicator added.
    """

    # Calculate ROCR
    history_df["ROCR"] = history_df["Close"] / history_df["Close"].shift(period)

    # Add ROCR trace to the plot with a unique color
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["ROCR"],
            mode="lines",
            line=dict(color="#1E90FF", width=2),
            name=f"ROCR ({period})",
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
            title="Rate of Change Ratio (ROCR)",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
