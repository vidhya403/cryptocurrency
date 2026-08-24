import streamlit as st
from concurrent.futures import ThreadPoolExecutor
from api_client import cg

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_coin_prices(coin: str, days: int) -> list:
    """Fetch price data for a single coin. Cached independently."""
    data = cg.get_coin_market_chart_by_id(id=coin, vs_currency='usd', days=days)
    return data['prices']

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_coin_market_data(coin: str, days: int):
    data = cg.get_coin_market_chart_by_id(id=coin, vs_currency='usd', days=days)
    return {
        "prices": data['prices'],
        "volumes": data['total_volumes']
    }

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_coin_ohlc(coin: str, days: int):
    if days <= 7:
        days = 7
    elif days <= 14:
        days = 14
    elif days <= 30:
        days = 30
    elif days <= 90:
        days = 90
    elif days <= 180:
        days = 180
    else:
        days = 365
    data = cg.get_coin_ohlc_by_id(id=coin, vs_currency='usd', days=days)
    return data

def fetch_multiple_coins(coins: list, days: int) -> dict:
    """Fetch multiple coins in parallel."""
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(lambda c: (c, fetch_coin_prices(c, days)), coins)
    return dict(results)
