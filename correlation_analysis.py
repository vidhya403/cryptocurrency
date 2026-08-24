# correlation_analysis.py
import pandas as pd
import plotly.express as px
from data_fetcher import fetch_multiple_coins
import datetime

def correlation_heatmap(coins: list, months: int):
    days = months * 30
    coin_data = fetch_multiple_coins(coins, days)
    
    # Build DataFrame with daily closing prices
    df = pd.DataFrame()
    for coin, prices in coin_data.items():
        temp = pd.DataFrame(prices, columns=['timestamp', coin])
        temp['timestamp'] = pd.to_datetime(temp['timestamp'], unit='ms')
        temp = temp.set_index('timestamp').resample('D').mean()
        df[coin] = temp[coin]
    
    corr = df.pct_change().corr()  # correlation of daily returns
    
    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        title=f"Correlation Heatmap ({months} months)"
    )
    return fig