# Imports
import pandas as pd
import plotly.graph_objects as go


# Function for Chaikin-like indicator without volume
def add_chaikin_ad_indicator(fig: go.Figure, history_df: pd.DataFrame) -> go.Figure:
    """Add a price-movement-based Chaikin-like indicator to the given plot.

    This is a workaround when volume data is not available.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.

    Returns:
        go.Figure: The plot with the modified Chaikin A/D-like indicator added.
    """

    # Calculate Price Range Multiplier
    history_df["PriceRangeMultiplier"] = (
        2 * history_df["Close"] - history_df["Low"] - history_df["High"]
    ) / (history_df["High"] - history_df["Low"]).replace(0, 1)

    # Estimate "pseudo-volume" as the range between high and low prices
    history_df["PseudoVolume"] = history_df["High"] - history_df["Low"]

    # Calculate the price-movement-based Chaikin A/D approximation
    history_df["ChaikinAD_NoVolume"] = (
        history_df["PriceRangeMultiplier"] * history_df["PseudoVolume"]
    ).cumsum()

    # Add the trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["ChaikinAD_NoVolume"],
            mode="lines",
            line=dict(color="#FF8C00", width=2),
            name="Chaikin A/D Approx (No Volume)",
            yaxis="y2",
        )
    )

    # Update layout for secondary Y-axis
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="Chaikin A/D Approx (No Volume)",
            overlaying="y",
            side="right",
        ),
    )

    return fig
