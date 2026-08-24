import plotly.graph_objects as go
from utils import get_price_volume_df

def volume_plot(coin, months):
    days = months * 30
    df = get_price_volume_df(coin, days)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df.index,
        y=df["volume"],
        name="Volume"
    ))

    fig.update_layout(title=f"{coin.title()} Volume Analysis")

    return fig