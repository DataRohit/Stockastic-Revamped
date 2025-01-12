# Imports
import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the Average Directional Index (ADX) Indicator
def add_adx_indicator(
    fig: go.Figure, history_df: pd.DataFrame, window: int = 14
) -> go.Figure:
    """Add the Average Directional Index (ADX) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The window size for calculating the ADX. Defaults to 14.

    Returns:
        go.Figure: The plot with the ADX indicator added.
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

    # Smooth TR, +DM, and -DM using an exponential moving average (EMA)
    history_df["TR_smoothed"] = history_df["TR"].rolling(window).mean()
    history_df["+DM_smoothed"] = history_df["+DM"].rolling(window).mean()
    history_df["-DM_smoothed"] = history_df["-DM"].rolling(window).mean()

    # Calculate +DI, -DI
    history_df["+DI"] = 100 * (history_df["+DM_smoothed"] / history_df["TR_smoothed"])
    history_df["-DI"] = 100 * (history_df["-DM_smoothed"] / history_df["TR_smoothed"])

    # Calculate DX and ADX
    history_df["DX"] = (
        100
        * abs(history_df["+DI"] - history_df["-DI"])
        / (history_df["+DI"] + history_df["-DI"])
    )
    history_df["ADX"] = history_df["DX"].rolling(window).mean()

    # Add +DI trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["+DI"],
            mode="lines",
            line=dict(color="#00FF00", width=2),
            name=f"+DI {window}",
            yaxis="y2",
        )
    )

    # Add -DI trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["-DI"],
            mode="lines",
            line=dict(color="#FF0000", width=2),
            name=f"-DI {window}",
            yaxis="y2",
        )
    )

    # Add ADX trace to the plot
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

    # Update layout for visibility
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="+DI / -DI / ADX",
            overlaying="y",
            side="right",
            range=[0, 100],
        ),
    )

    # Return the figure
    return fig
