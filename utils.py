import pandas as pd
from data_fetcher import fetch_coin_prices
from data_fetcher import fetch_coin_market_data

def get_price_df(coin, days):
    data = fetch_coin_prices(coin, days)

    df = pd.DataFrame(data, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    return df

def get_price_volume_df(coin, days):
    data = fetch_coin_market_data(coin, days)

    import pandas as pd

    price_df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    vol_df = pd.DataFrame(data["volumes"], columns=["timestamp", "volume"])

    df = price_df.merge(vol_df, on="timestamp")

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    return df