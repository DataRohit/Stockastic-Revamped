# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate and plot Chaikin A/D Oscillator (ADOSC) without volume
def add_adosc_indicator(
    fig: go.Figure,
    history_df: pd.DataFrame,
    short_period: int = 3,
    long_period: int = 10,
) -> go.Figure:
    """Add Chaikin A/D Oscillator (ADOSC) approximation to the given plot (without volume).

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        short_period (int, optional): The short period EMA for ADOSC calculation. Defaults to 3.
        long_period (int, optional): The long period EMA for ADOSC calculation. Defaults to 10.

    Returns:
        go.Figure: The plot with ADOSC approximation added.
    """

    # Calculate Price Range Multiplier (Money Flow Multiplier approximation)
    history_df["PriceRangeMultiplier"] = (
        2 * history_df["Close"] - history_df["Low"] - history_df["High"]
    ) / (history_df["High"] - history_df["Low"]).replace(0, 1)

    # Use price range as a pseudo-volume approximation
    history_df["PseudoVolume"] = history_df["High"] - history_df["Low"]

    # Calculate Chaikin A/D approximation
    history_df["ChaikinAD_NoVolume"] = (
        history_df["PriceRangeMultiplier"] * history_df["PseudoVolume"]
    ).cumsum()

    # Calculate short and long period EMAs for ADOSC
    history_df["ADOSC"] = (
        history_df["ChaikinAD_NoVolume"].ewm(span=short_period, adjust=False).mean()
        - history_df["ChaikinAD_NoVolume"].ewm(span=long_period, adjust=False).mean()
    )

    # Add ADOSC trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["ADOSC"],
            mode="lines",
            line=dict(color="#FF1493", width=2),
            name=f"ADOSC ({short_period}, {long_period})",
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
            title="Chaikin A/D Oscillator (No Volume)",
            overlaying="y",
            side="right",
        ),
    )

    return fig
