import datetime
import plotly.graph_objects as go
from data_fetcher import fetch_multiple_coins

def show_normalized(coins: list, days: int):
    coin_data = fetch_multiple_coins(coins, days)
    
    fig = go.Figure()
    for coin, prices in coin_data.items():
        dates = [datetime.datetime.fromtimestamp(p[0] / 1000) for p in prices]
        values = [p[1] for p in prices]
        normalized = [(v / values[0]) * 100 for v in values]
        
        fig.add_trace(go.Scatter(x=dates, y=normalized, mode='lines', name=coin))
    
    fig.update_layout(
        title="Normalized Crypto Trends",
        xaxis_title="Date",
        yaxis_title="Growth (Base = 100)"
    )
    return fig
