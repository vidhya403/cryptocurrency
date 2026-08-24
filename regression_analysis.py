import pandas as pd
from data_fetcher import fetch_multiple_coins
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def regression_profit_prediction(coins: list, months: int):
    days = months * 30
    coin_data = fetch_multiple_coins(coins, days)

    returns = {}
    risks = {}

    # -------------------------
    # Prepare Data
    # -------------------------
    for coin, prices in coin_data.items():
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df.set_index('timestamp').resample('D').mean()

        df['return'] = df['price'].pct_change()
        df = df.dropna()

        returns[coin] = df['return']
        risks[coin] = df['return'].std()

    df_returns = pd.DataFrame(returns).dropna()

    # -------------------------
    # Train-Test Split
    # -------------------------
    split = int(len(df_returns) * 0.8)

    X = df_returns.iloc[:-1]
    y = df_returns.shift(-1).iloc[:-1]

    X_train = X.iloc[:split]
    X_test = X.iloc[split:]

    y_train = y.iloc[:split]
    y_test = y.iloc[split:]

    predictions = {}
    mse_scores = {}

    # -------------------------
    # Train Model
    # -------------------------
    for coin in coins:
        model = LinearRegression()

        model.fit(X_train.drop(columns=coin), y_train[coin])

        y_pred = model.predict(X_test.drop(columns=coin))

        mse = mean_squared_error(y_test[coin], y_pred)

        mse_scores[coin] = mse
        predictions[coin] = y_pred[-1]

    # -------------------------
    # Result Table
    # -------------------------
    df_result = pd.DataFrame({
        "Coin": coins,
        "Predicted Return": [predictions[c] for c in coins],
        "Risk (Volatility)": [risks[c] for c in coins],
        "Model Error (MSE)": [mse_scores[c] for c in coins]
    })

    # Investment Score
    df_result["Score"] = df_result["Predicted Return"] / df_result["Risk (Volatility)"]

    # -------------------------
    # Quadrant Logic
    # -------------------------
    mean_risk = df_result["Risk (Volatility)"].mean()
    mean_return = df_result["Predicted Return"].mean()

    def categorize(row):
        if row["Predicted Return"] > mean_return and row["Risk (Volatility)"] < mean_risk:
            return "Best (High Return, Low Risk)"
        elif row["Predicted Return"] > mean_return:
            return "High Return (High Risk)"
        elif row["Risk (Volatility)"] < mean_risk:
            return "Safe (Low Risk)"
        else:
            return "Avoid"

    df_result["Category"] = df_result.apply(categorize, axis=1)

    df_result = df_result.sort_values("Score", ascending=False)

    # -------------------------
    # 1. Improved Scatter Plot
    # -------------------------
    fig_scatter = px.scatter(
        df_result,
        x="Risk (Volatility)",
        y="Predicted Return",
        text="Coin",
        color="Category",
        size="Model Error (MSE)",
        title="Risk vs Predicted Return (Decision Zones)"
    )

    fig_scatter.update_traces(textposition='top center')

    # Add quadrant lines
    fig_scatter.add_vline(x=mean_risk, line_dash="dash")
    fig_scatter.add_hline(y=mean_return, line_dash="dash")

    fig_scatter.update_layout(
        xaxis_title="Risk (Lower is Better)",
        yaxis_title="Predicted Return (Higher is Better)"
    )

    # -------------------------
    # 2. Ranking Bar Chart
    # -------------------------
    fig_bar = px.bar(
        df_result,
        x="Coin",
        y="Score",
        color="Category",
        title="Investment Ranking (Best Coins)"
    )

    # -------------------------
    # 3. Actual vs Predicted
    # -------------------------
    coin0 = coins[0]

    model = LinearRegression()
    model.fit(X_train.drop(columns=coin0), y_train[coin0])

    y_pred_full = model.predict(X_test.drop(columns=coin0))

    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(
        y=y_test[coin0].values,
        mode='lines',
        name='Actual'
    ))

    fig_line.add_trace(go.Scatter(
        y=y_pred_full,
        mode='lines',
        name='Predicted'
    ))

    fig_line.update_layout(
        title=f"Actual vs Predicted Returns ({coin0})",
        xaxis_title="Time",
        yaxis_title="Return"
    )

    return df_result, fig_scatter, fig_bar, fig_line