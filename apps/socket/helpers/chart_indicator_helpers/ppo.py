# Imports
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the PPO (Percentage Price Oscillator) Indicator
def add_ppo_indicator(
    fig: go.Figure,
    history_df: pd.DataFrame,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> go.Figure:
    """Add the Percentage Price Oscillator (PPO) indicator to the given plot.

    Args:
        fig (go.Figure): The plot to which the indicator will be added.
        history_df (pd.DataFrame): The historical stock data.
        fast_period (int, optional): The period for the fast EMA. Defaults to 12.
        slow_period (int, optional): The period for the slow EMA. Defaults to 26.
        signal_period (int, optional): The period for the signal line EMA. Defaults to 9.

    Returns:
        go.Figure: The plot with the PPO indicator added.
    """

    # Calculate the fast and slow EMAs
    history_df["EMA_Fast"] = (
        history_df["Close"].ewm(span=fast_period, adjust=False).mean()
    )
    history_df["EMA_Slow"] = (
        history_df["Close"].ewm(span=slow_period, adjust=False).mean()
    )

    # Calculate the PPO
    history_df["PPO"] = (
        (history_df["EMA_Fast"] - history_df["EMA_Slow"]) / history_df["EMA_Slow"]
    ) * 100

    # Calculate the PPO signal line (EMA of PPO)
    history_df["PPO_Signal"] = (
        history_df["PPO"].ewm(span=signal_period, adjust=False).mean()
    )

    # Add PPO trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["PPO"],
            mode="lines",
            line=dict(color="#FFA500", width=2),
            name=f"PPO ({fast_period}, {slow_period})",
            yaxis="y2",
        )
    )

    # Add PPO signal line trace to the plot
    fig.add_trace(
        go.Scatter(
            x=history_df.index,
            y=history_df["PPO_Signal"],
            mode="lines",
            line=dict(color="#1f77b4", width=2, dash="dot"),
            name=f"PPO Signal ({signal_period})",
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
            title="PPO / Signal Line",
            overlaying="y",
            side="right",
        ),
    )

    # Return the figure
    return fig
