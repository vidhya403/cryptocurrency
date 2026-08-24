import datetime
import plotly.graph_objects as go
from data_fetcher import fetch_coin_prices

def show_duration(coin: str, months: int):
    days = months * 30
    prices = fetch_coin_prices(coin, days)
    
    dates = [datetime.datetime.fromtimestamp(p[0] / 1000) for p in prices]
    values = [p[1] for p in prices]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=values, mode='lines', name=coin))
    fig.update_layout(
        title=f"{coin.title()} Price — Last {months} Months",
        xaxis_title="Date",
        yaxis_title="Price (USD)"
    )
    return fig
