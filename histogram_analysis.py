import pandas as pd
import plotly.express as px
from data_fetcher import fetch_multiple_coins

def returns_histogram(coins: list, months: int):
    days = months * 30
    coin_data = fetch_multiple_coins(coins, days)
    
    df = pd.DataFrame()
    stats = []

    for coin, prices in coin_data.items():
        temp = pd.DataFrame(prices, columns=['timestamp', coin])
        temp['timestamp'] = pd.to_datetime(temp['timestamp'], unit='ms')
        temp = temp.set_index('timestamp').resample('D').mean()

        returns = temp[coin].pct_change().dropna()
        df[coin] = returns

        # 📊 Calculate risk and return
        avg_return = returns.mean()
        risk = returns.std()

        stats.append({
            "Coin": coin,
            "Average Return": avg_return,
            "Risk (Volatility)": risk
        })

    # -------------------------
    # Histogram
    # -------------------------
    df_melt = df.dropna().melt(var_name='Coin', value_name='Daily Return')

    fig_hist = px.histogram(
        df_melt,
        x='Daily Return',
        color='Coin',
        barmode='overlay',
        marginal='box',
        nbins=50,
        title=f"Histogram of Daily Returns ({months} months)"
    )

    # -------------------------
    # Risk vs Return Plot
    # -------------------------
    stats_df = pd.DataFrame(stats)

    fig_scatter = px.scatter(
        stats_df,
        x="Risk (Volatility)",
        y="Average Return",
        text="Coin",
        title="Risk vs Return Analysis"
    )

    fig_scatter.update_traces(textposition='top center')

    return fig_hist, fig_scatter, stats_df