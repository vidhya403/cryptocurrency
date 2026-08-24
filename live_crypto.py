import datetime
import streamlit as st
import plotly.graph_objects as go
from api_client import cg

@st.cache_data(ttl=60, show_spinner=False)  # shorter TTL for live data
def fetch_today_prices(coin: str) -> list:
    data = cg.get_coin_market_chart_by_id(id=coin, vs_currency='usd', days=1)
    return data['prices']

def get_today_coin_plot(coin: str):
    prices = fetch_today_prices(coin)
    
    dates = [datetime.datetime.fromtimestamp(p[0] / 1000) for p in prices]
    values = [p[1] for p in prices]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=values, mode='lines', name=coin))
    fig.update_layout(
        title=f"{coin.upper()} — Today",
        xaxis_title="Time",
        yaxis_title="Price (USD)",
        hovermode="x unified"
    )
    return fig
