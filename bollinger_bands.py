import plotly.graph_objects as go
from utils import get_price_df

def bollinger_plot(coin, months, window=20):
    days = months * 30
    df = get_price_df(coin, days)

    price = df["price"]

    sma = price.rolling(window).mean()
    std = price.rolling(window).std()

    upper = sma + 2 * std
    lower = sma - 2 * std

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df.index, y=price, name="Price"))
    fig.add_trace(go.Scatter(x=df.index, y=sma, name="SMA"))
    fig.add_trace(go.Scatter(x=df.index, y=upper, name="Upper Band"))
    fig.add_trace(go.Scatter(x=df.index, y=lower, name="Lower Band"))

    fig.update_layout(title=f"{coin.title()} Bollinger Bands")

    return fig