# Imports
from concurrent.futures import ThreadPoolExecutor

import plotly.graph_objects as go
import yfinance as yf

from apps.socket.helpers.chart_indicator_helpers import (
    add_dema_indicator,
    add_ema_indicator,
    add_kama_indicator,
    add_mama_indicator,
    add_sma_indicator,
    add_tema_indicator,
    add_trima_indicator,
    add_wma_indicator,
)
from apps.socket.utils import fetch_ticker_data


# Function to generate candlestick chart
def generate_candlestick_chart(
    symbol: str,
    period: str = "1d",
    interval: str = "5m",
    indicator: str = "none",
    height: int = 650,
) -> go.Figure:
    """Generate a candlestick plot for the given stock symbol."""

    # Initialize the ticker
    ticker = yf.Ticker(symbol)

    # Use ThreadPoolExecutor to fetch info and history concurrently
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_info = executor.submit(fetch_ticker_data, ticker, "info")
        future_history = executor.submit(
            fetch_ticker_data, ticker, "history", period, interval
        )

        # Wait for both futures to complete
        info = future_info.result()
        history_df = future_history.result()

    # Round the values to 2 decimal places
    history_df = history_df.round(2)

    # Create the candlestick plot
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=history_df.index,
                open=history_df["Open"],
                high=history_df["High"],
                low=history_df["Low"],
                close=history_df["Close"],
                name="Candlestick",
            )
        ]
    )

    # Add a horizontal line for the previous close
    previous_close = info.get("previousClose", None)
    if previous_close:
        fig.add_shape(
            type="line",
            x0=history_df.index.min(),
            x1=history_df.index.max(),
            y0=previous_close,
            y1=previous_close,
            line=dict(
                color="lightgray",
                width=1.5,
                dash="dash",
            ),
        )

        # Add annotation for the previous close line
        fig.add_annotation(
            x=history_df.index.min(),
            y=previous_close,
            text=f"Previous Close: {previous_close}",
            showarrow=False,
            font=dict(color="lightgray", size=12, family="JetBrains Mono"),
            align="center",
            yanchor="bottom",
            xanchor="left",
        )

    # Match the indicator
    match indicator:
        # If indicator is "sma"
        case "sma":
            # Add the SMA indicator
            fig = add_sma_indicator(fig, history_df, 20)

        # If indicator is "ema"
        case "ema":
            # Add the EMA indicator
            fig = add_ema_indicator(fig, history_df, 20)

        # If indicator is "wma"
        case "wma":
            # Add the WMA indicator
            fig = add_wma_indicator(fig, history_df, 20)

        # If indicator is "dema"
        case "dema":
            # Add the DEMA indicator
            fig = add_dema_indicator(fig, history_df, 20)

        # If indicator is "tema"
        case "tema":
            # Add the TEMA indicator
            fig = add_tema_indicator(fig, history_df, 20)

        # If indicator is "trima"
        case "trima":
            # Add the TRIMA indicator
            fig = add_trima_indicator(fig, history_df, 20)

        # If indicator is "kama"
        case "kama":
            # Add the KAMA indicator
            fig = add_kama_indicator(fig, history_df, 20)

        # If indicator is "mama"
        case "mama":
            # Add the MAMA indicator
            fig = add_mama_indicator(fig, history_df, 20)

    # Update the layout with Tailwind bg-base-100 color
    fig.update_layout(
        title="Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        plot_bgcolor="#1d232a",
        paper_bgcolor="#1d232a",
        font=dict(
            color="#ffffff",
            family="JetBrains Mono",
            size=12,
        ),
        xaxis=dict(
            gridcolor="#333333",
            zerolinecolor="#333333",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
            rangeslider_visible=False,
        ),
        yaxis=dict(
            gridcolor="#333333",
            zerolinecolor="#333333",
            title_font=dict(family="JetBrains Mono"),
            tickfont=dict(family="JetBrains Mono"),
        ),
        hoverlabel=dict(font=dict(family="JetBrains Mono"), namelength=-1),
        height=height,
    )

    # Update the hover labels to be capitalized
    fig.data[0].text = [
        f"Date: {x}<br>"
        + f"Open: {o}<br>"
        + f"High: {h}<br>"
        + f"Low: {l}<br>"
        + f"Close: {c}"
        for x, o, h, l, c in zip(
            history_df.index,
            history_df["Open"],
            history_df["High"],
            history_df["Low"],
            history_df["Close"],
        )
    ]
    fig.data[0].hoverinfo = "text"

    # Return the figure
    return fig
