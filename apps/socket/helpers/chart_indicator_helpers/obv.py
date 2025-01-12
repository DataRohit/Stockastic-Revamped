# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate a price-based OBV-like indicator
def add_price_based_obv_indicator(
    fig: go.Figure, history_df: pd.DataFrame
) -> go.Figure:
    """Add a price-based OBV-like indicator to the plot (without volume data).

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.

    Returns:
        go.Figure: The plot with the price-based OBV-like indicator added.
    """

    # Initialize OBV-like with 0 for the first value
    obv_like = [0]

    # Loop through historical data to calculate the price-based OBV-like
    for i in range(1, len(history_df)):
        if history_df["Close"].iloc[i] > history_df["Close"].iloc[i - 1]:
            obv_like.append(obv_like[-1] + 1)  # Increment for price rise
        elif history_df["Close"].iloc[i] < history_df["Close"].iloc[i - 1]:
            obv_like.append(obv_like[-1] - 1)  # Decrement for price fall
        else:
            obv_like.append(obv_like[-1])  # No change if price is unchanged

    # Add price-based OBV-like as a new column
    history_df["PriceBasedOBV"] = obv_like

    # Define a bright color for the price-based OBV-like line
    obv_color = "#00BFFF"  # Deep Sky Blue

    # Add the price-based OBV-like trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["PriceBasedOBV"],
            mode="lines",
            line=dict(color=obv_color, width=2),
            name="Price-Based OBV",
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
            title="Price-Based OBV-Like",
            overlaying="y",
            side="right",
        ),
    )

    return fig
