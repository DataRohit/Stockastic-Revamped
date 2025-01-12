# Imports
import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the ADXR Indicator
def add_adxr_indicator(
    fig: go.Figure, history_df: pd.DataFrame, window: int = 14
) -> go.Figure:
    """Add the Average Directional Movement Rating (ADXR) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The window size for calculating the ADX and ADXR. Defaults to 14.

    Returns:
        go.Figure: The plot with the ADXR indicator added.
    """

    # Calculate True Range (TR)
    history_df["H-L"] = history_df["High"] - history_df["Low"]
    history_df["H-PC"] = abs(history_df["High"] - history_df["Close"].shift(1))
    history_df["L-PC"] = abs(history_df["Low"] - history_df["Close"].shift(1))
    history_df["TR"] = history_df[["H-L", "H-PC", "L-PC"]].max(axis=1)

    # Calculate +DM and -DM
    history_df["+DM"] = np.where(
        (history_df["High"].diff() > history_df["Low"].diff())
        & (history_df["High"].diff() > 0),
        history_df["High"].diff(),
        0,
    )
    history_df["-DM"] = np.where(
        (history_df["Low"].diff() > history_df["High"].diff())
        & (history_df["Low"].diff() > 0),
        -history_df["Low"].diff(),
        0,
    )

    # Smooth TR, +DM, and -DM
    history_df["TR_smoothed"] = history_df["TR"].rolling(window).mean()
    history_df["+DM_smoothed"] = history_df["+DM"].rolling(window).mean()
    history_df["-DM_smoothed"] = history_df["-DM"].rolling(window).mean()

    # Calculate +DI and -DI
    history_df["+DI"] = 100 * (history_df["+DM_smoothed"] / history_df["TR_smoothed"])
    history_df["-DI"] = 100 * (history_df["-DM_smoothed"] / history_df["TR_smoothed"])

    # Calculate DX and ADX
    history_df["DX"] = (
        100
        * abs(history_df["+DI"] - history_df["-DI"])
        / (history_df["+DI"] + history_df["-DI"])
    )
    history_df["ADX"] = history_df["DX"].rolling(window).mean()

    # Calculate ADXR (average of current and past ADX values)
    history_df["ADXR"] = (history_df["ADX"] + history_df["ADX"].shift(window)) / 2

    # Add ADX trace to the plot for reference
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["ADX"],
            mode="lines",
            line=dict(color="#1f77b4", width=2, dash="dot"),
            name=f"ADX {window}",
            yaxis="y2",
        )
    )

    # Add ADXR trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["ADXR"],
            mode="lines",
            line=dict(color="#FFA500", width=2),
            name=f"ADXR {window}",
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
            title="ADX / ADXR",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
