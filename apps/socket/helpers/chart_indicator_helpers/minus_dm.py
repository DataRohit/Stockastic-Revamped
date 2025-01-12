# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the -DM (Negative Directional Movement) indicator
def add_minus_dm_indicator(
    fig: go.Figure, history_df: pd.DataFrame, period: int = 14
) -> go.Figure:
    """Add the -DM (Negative Directional Movement) to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        period (int, optional): The period for calculating the -DM. Defaults to 14.

    Returns:
        go.Figure: The plot with the -DM indicator added.
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

    # Smooth the -DM and TR over the period
    history_df["-DM_smooth"] = history_df["-DM"].rolling(window=period).sum()
    history_df["TR_smooth"] = history_df["TR"].rolling(window=period).sum()

    # Add -DM trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["-DM_smooth"],
            mode="lines",
            line=dict(color="#FF1493", width=2),
            name=f"-DM ({period})",
            yaxis="y2",
        )
    )

    # Update layout to add secondary Y-axis for -DM
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="-DM (Negative Directional Movement)",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
