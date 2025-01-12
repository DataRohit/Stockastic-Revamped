# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the DX (Directional Movement) indicator
def add_dx_indicator(
    fig: go.Figure, history_df: pd.DataFrame, period: int = 14
) -> go.Figure:
    """Add the DX (Directional Movement) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        period (int, optional): The period for calculating the DX. Defaults to 14.

    Returns:
        go.Figure: The plot with the DX indicator added.
    """

    # Calculate +DM and -DM
    history_df["+DM"] = history_df["High"].diff()
    history_df["-DM"] = history_df["Low"].diff().abs()

    # Calculate the True Range (TR)
    history_df["TR"] = history_df[["High", "Low", "Close"]].max(axis=1) - history_df[
        ["High", "Low", "Close"]
    ].min(axis=1)

    # Apply the conditions for +DM and -DM
    history_df["+DM"] = history_df.apply(
        lambda x: x["+DM"] if x["+DM"] > 0 and x["+DM"] > x["-DM"] else 0, axis=1
    )
    history_df["-DM"] = history_df.apply(
        lambda x: x["-DM"] if x["-DM"] > 0 and x["-DM"] > x["+DM"] else 0, axis=1
    )

    # Smooth the +DM, -DM, and TR over the period
    history_df["+DM_smooth"] = history_df["+DM"].rolling(window=period).sum()
    history_df["-DM_smooth"] = history_df["-DM"].rolling(window=period).sum()
    history_df["TR_smooth"] = history_df["TR"].rolling(window=period).sum()

    # Calculate +DI and -DI
    history_df["+DI"] = (history_df["+DM_smooth"] / history_df["TR_smooth"]) * 100
    history_df["-DI"] = (history_df["-DM_smooth"] / history_df["TR_smooth"]) * 100

    # Calculate DX
    history_df["DX"] = (
        abs(history_df["+DI"] - history_df["-DI"])
        / (history_df["+DI"] + history_df["-DI"])
        * 100
    )

    # Add DX trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["DX"],
            mode="lines",
            line=dict(color="#FFD500", width=2),
            name=f"DX ({period})",
            yaxis="y2",
        )
    )

    # Update layout to add secondary Y-axis for DX
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="DX (Directional Movement)",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
