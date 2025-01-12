# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the Aroon Indicator
def add_aroon_indicator(
    fig: go.Figure, history_df: pd.DataFrame, period: int = 14
) -> go.Figure:
    """Add the Aroon Indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        period (int, optional): The lookback period for calculating the Aroon. Defaults to 14.

    Returns:
        go.Figure: The plot with the Aroon indicator added.
    """

    # Calculate Aroon Up and Aroon Down
    history_df["Aroon Up"] = (
        100
        * (
            period
            - history_df["Close"]
            .rolling(window=period)
            .apply(lambda x: x[::-1].argmax(), raw=False)
        )
        / period
    )
    history_df["Aroon Down"] = (
        100
        * (
            period
            - history_df["Close"]
            .rolling(window=period)
            .apply(lambda x: x[::-1].argmin(), raw=False)
        )
        / period
    )

    # Add Aroon Up trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["Aroon Up"],
            mode="lines",
            line=dict(color="#1E90FF", width=2),
            name=f"Aroon Up ({period})",
            yaxis="y2",
        )
    )

    # Add Aroon Down trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["Aroon Down"],
            mode="lines",
            line=dict(color="#FF6347", width=2),
            name=f"Aroon Down ({period})",
            yaxis="y2",
        )
    )

    # Update layout to add secondary Y-axis for Aroon
    fig.update_layout(
        yaxis2=dict(
            gridcolor="#888888",
            zerolinecolor="#888888",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            title="Aroon Indicator",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
