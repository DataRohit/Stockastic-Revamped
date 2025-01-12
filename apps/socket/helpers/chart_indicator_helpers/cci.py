# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the CCI (Commodity Channel Index) Indicator
def add_cci_indicator(
    fig: go.Figure, history_df: pd.DataFrame, window: int = 20
) -> go.Figure:
    """Add the Commodity Channel Index (CCI) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        window (int, optional): The lookback period for calculating the CCI. Defaults to 20.

    Returns:
        go.Figure: The plot with the CCI indicator added.
    """

    # Calculate the typical price
    history_df["Typical_Price"] = (
        history_df["High"] + history_df["Low"] + history_df["Close"]
    ) / 3

    # Calculate the moving average of the typical price
    history_df["TP_MA"] = history_df["Typical_Price"].rolling(window).mean()

    # Calculate the mean deviation using a custom method
    history_df["Mean_Deviation"] = (
        history_df["Typical_Price"]
        .rolling(window)
        .apply(lambda x: abs(x - x.mean()).mean(), raw=False)
    )

    # Calculate the CCI
    history_df["CCI"] = (history_df["Typical_Price"] - history_df["TP_MA"]) / (
        0.015 * history_df["Mean_Deviation"]
    )

    # Add CCI trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["CCI"],
            mode="lines",
            line=dict(color="#FFA500", width=2),
            name=f"CCI ({window})",
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
            title="Commodity Channel Index (CCI)",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
