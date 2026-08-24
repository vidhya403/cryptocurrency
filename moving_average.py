# moving_average.py
import pandas as pd
import plotly.graph_objects as go
from data_fetcher import fetch_coin_prices

def moving_average_plot(coin: str, months: int, window: int = 7):
    days = months * 30
    prices = fetch_coin_prices(coin, days)
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.set_index('timestamp').resample('D').mean()
    
    df['MA'] = df['price'].rolling(window=window).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['price'], mode='lines', name=f'{coin} Price'))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA'], mode='lines', name=f'{window}-Day MA'))
    fig.update_layout(
        title=f"{coin.upper()} Moving Average ({window}-Day) — Last {months} Months",
        xaxis_title="Date",
        yaxis_title="Price (USD)"
    )
    return fig