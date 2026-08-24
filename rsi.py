import plotly.graph_objects as go
from utils import get_price_df

def rsi_plot(coin, months, period=14):
    days = months * 30
    df = get_price_df(coin, days)

    close = df["price"]

    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=rsi, name="RSI"))

    fig.add_hline(y=70, line_dash="dash", annotation_text="Overbought")
    fig.add_hline(y=30, line_dash="dash", annotation_text="Oversold")

    fig.update_layout(title=f"{coin.title()} RSI")

    return fig