# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the CMO (Chande Momentum Oscillator) Indicator
def add_cmo_indicator(
    fig: go.Figure, history_df: pd.DataFrame, period: int = 14
) -> go.Figure:
    """Add the Chande Momentum Oscillator (CMO) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        period (int, optional): The lookback period for calculating the CMO. Defaults to 14.

    Returns:
        go.Figure: The plot with the CMO indicator added.
    """

    # Calculate price changes
    history_df["Price_Change"] = history_df["Close"].diff()

    # Calculate gains and losses
    history_df["Gain"] = history_df["Price_Change"].clip(lower=0)
    history_df["Loss"] = -history_df["Price_Change"].clip(upper=0)

    # Calculate sum of gains and losses over the lookback period
    history_df["Sum_Gain"] = history_df["Gain"].rolling(period).sum()
    history_df["Sum_Loss"] = history_df["Loss"].rolling(period).sum()

    # Calculate CMO
    history_df["CMO"] = (
        100
        * (history_df["Sum_Gain"] - history_df["Sum_Loss"])
        / (history_df["Sum_Gain"] + history_df["Sum_Loss"])
    )

    # Add CMO trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["CMO"],
            mode="lines",
            line=dict(color="#FFA500", width=2),
            name=f"CMO ({period})",
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
            title="Chande Momentum Oscillator (CMO)",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
