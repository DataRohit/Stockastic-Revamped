# Imports
from concurrent.futures import ThreadPoolExecutor

import plotly.graph_objects as go
import yfinance as yf

from apps.socket.helpers.chart_indicator_helpers import *
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

    # Define a mapping of indicators to functions
    indicator_functions = {
        "sma": add_sma_indicator,
        "ema": add_ema_indicator,
        "wma": add_wma_indicator,
        "dema": add_dema_indicator,
        "tema": add_tema_indicator,
        "trima": add_trima_indicator,
        "kama": add_kama_indicator,
        "mama": add_mama_indicator,
        "t3": add_t3_indicator,
        "macd": add_macd_indicator,
        "stoch": add_stochastic_indicator,
        "stochf": add_stochastic_fast_indicator,
        "rsi": add_rsi_indicator,
        "stochrsi": add_stochastic_rsi_indicator,
        "willr": add_williams_r_indicator,
        "adxr": add_adxr_indicator,
        "apo": add_apo_indicator,
        "ppo": add_ppo_indicator,
        "mom": add_mom_indicator,
        "bop": add_bop_indicator,
        "cci": add_cci_indicator,
        "cmo": add_cmo_indicator,
        "roc": add_roc_indicator,
        "rocr": add_rocr_indicator,
        "aroon": add_aroon_indicator,
    }

    # If the indicator is in the mapping
    if indicator in indicator_functions:
        # Call the function to add the indicator to the figure
        fig = indicator_functions[indicator](fig, history_df)

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
