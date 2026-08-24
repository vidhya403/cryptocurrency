import plotly.graph_objects as go
import pandas as pd
from data_fetcher import fetch_coin_ohlc

def candlestick_plot(coin, months):
    days = months * 30

    data = fetch_coin_ohlc(coin, days)

    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])

    fig.update_layout(
        title=f"{coin.title()} Candlestick Chart",
        xaxis_rangeslider_visible=False
    )

    return fig