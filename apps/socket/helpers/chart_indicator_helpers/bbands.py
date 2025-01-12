# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the Bollinger Bands (BBands) indicator
def add_bbands_indicator(
    fig: go.Figure, history_df: pd.DataFrame, period: int = 20, std_dev: int = 2
) -> go.Figure:
    """Add the Bollinger Bands (BBands) to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        period (int, optional): The period for calculating the moving average and bands. Defaults to 20.
        std_dev (int, optional): The number of standard deviations for the bands. Defaults to 2.

    Returns:
        go.Figure: The plot with the Bollinger Bands indicator added.
    """

    # Calculate the moving average (SMA) and standard deviation
    history_df["SMA"] = history_df["Close"].rolling(window=period).mean()
    history_df["STD"] = history_df["Close"].rolling(window=period).std()

    # Calculate the upper and lower Bollinger Bands
    history_df["UpperBand"] = history_df["SMA"] + (history_df["STD"] * std_dev)
    history_df["LowerBand"] = history_df["SMA"] - (history_df["STD"] * std_dev)

    # Add Upper Band trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["UpperBand"],
            mode="lines",
            line=dict(color="#FF6347", width=2, dash="dot"),
            name=f"Upper Band ({period})",
            yaxis="y2",
        )
    )

    # Add Lower Band trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["LowerBand"],
            mode="lines",
            line=dict(color="#1E90FF", width=2, dash="dot"),
            name=f"Lower Band ({period})",
            yaxis="y2",
        )
    )

    # Add SMA trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["SMA"],
            mode="lines",
            line=dict(color="#FFD700", width=2),
            name=f"SMA ({period})",
            yaxis="y2",
        )
    )

    # Update layout to add secondary Y-axis for Bollinger Bands
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="Bollinger Bands",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
