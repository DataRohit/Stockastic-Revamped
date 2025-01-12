# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the Ultimate Oscillator (UltOsc) indicator
def add_ultosc_indicator(
    fig: go.Figure,
    history_df: pd.DataFrame,
    short_period: int = 7,
    medium_period: int = 14,
    long_period: int = 28,
) -> go.Figure:
    """Add the Ultimate Oscillator (UltOsc) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        short_period (int, optional): The short period for calculating the BP and TR. Defaults to 7.
        medium_period (int, optional): The medium period for calculating the BP and TR. Defaults to 14.
        long_period (int, optional): The long period for calculating the BP and TR. Defaults to 28.

    Returns:
        go.Figure: The plot with the Ultimate Oscillator indicator added.
    """

    # Calculate the Buying Pressure (BP)
    history_df["Prev_Close"] = history_df["Close"].shift(
        1
    )  # Create shifted column for previous Close
    history_df["BP"] = history_df["Close"] - history_df[["Low", "Prev_Close"]].min(
        axis=1
    )

    # Calculate the True Range (TR)
    history_df["Prev_Close_Shifted"] = history_df["Close"].shift(1)
    history_df["TR"] = history_df[["High", "Prev_Close_Shifted"]].max(
        axis=1
    ) - history_df[["Low", "Prev_Close_Shifted"]].min(axis=1)

    # Calculate the smoothed BP and TR for the three different periods (short, medium, long)
    history_df["BP_short"] = history_df["BP"].rolling(window=short_period).sum()
    history_df["TR_short"] = history_df["TR"].rolling(window=short_period).sum()

    history_df["BP_medium"] = history_df["BP"].rolling(window=medium_period).sum()
    history_df["TR_medium"] = history_df["TR"].rolling(window=medium_period).sum()

    history_df["BP_long"] = history_df["BP"].rolling(window=long_period).sum()
    history_df["TR_long"] = history_df["TR"].rolling(window=long_period).sum()

    # Calculate the Ultimate Oscillator (UltOsc)
    history_df["UltOsc"] = (
        4 * history_df["BP_short"] * history_df["TR_short"]
        + 2 * history_df["BP_medium"] * history_df["TR_medium"]
        + history_df["BP_long"] * history_df["TR_long"]
    ) / (
        4 * history_df["TR_short"] + 2 * history_df["TR_medium"] + history_df["TR_long"]
    )

    # Add UltOsc trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["UltOsc"],
            mode="lines",
            line=dict(color="#FFD700", width=2),
            name=f"Ultimate Oscillator ({short_period}, {medium_period}, {long_period})",
            yaxis="y2",
        )
    )

    # Update layout to add secondary Y-axis for UltOsc
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="Ultimate Oscillator",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
