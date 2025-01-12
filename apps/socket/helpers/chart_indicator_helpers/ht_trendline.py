# Imports
import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the HT_TRENDLINE (Hilbert Transform - Instantaneous Trendline)
def add_ht_trendline(fig: go.Figure, history_df: pd.DataFrame) -> go.Figure:
    """Add the HT_TRENDLINE (Hilbert Transform - Instantaneous Trendline) to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.

    Returns:
        go.Figure: The plot with the HT_TRENDLINE indicator added.
    """

    # Calculate the Hilbert Transform - Instantaneous Trendline (HT_TRENDLINE)
    # First, calculate the Hilbert Transform of the Close price
    close_prices = history_df["Close"].values
    n = len(close_prices)

    # Applying the Hilbert Transform
    HT = np.fft.fft(close_prices)
    transform = np.fft.ifft(HT)

    # Extract the real part of the transform (this represents the trendline)
    trendline = transform.real

    # Add the trendline to the dataframe
    history_df["HT_TRENDLINE"] = trendline

    # Add the HT_TRENDLINE trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["HT_TRENDLINE"],
            mode="lines",
            line=dict(color="#FFD700", width=2),
            name="HT Trendline",
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
            title="Hilbert Transform - Instantaneous Trendline",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
