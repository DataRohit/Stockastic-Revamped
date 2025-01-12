# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the MOM (Momentum) Indicator
def add_mom_indicator(
    fig: go.Figure, history_df: pd.DataFrame, period: int = 10
) -> go.Figure:
    """Add the Momentum (MOM) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        period (int, optional): The lookback period for calculating the MOM. Defaults to 10.

    Returns:
        go.Figure: The plot with the MOM indicator added.
    """

    # Calculate the MOM indicator
    history_df["MOM"] = history_df["Close"] - history_df["Close"].shift(period)

    # Add MOM trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["MOM"],
            mode="lines",
            line=dict(color="#FFA500", width=2),
            name=f"MOM ({period})",
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
            title="Momentum (MOM)",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
