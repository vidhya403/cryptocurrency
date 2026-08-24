import streamlit as st
from streamlit_autorefresh import st_autorefresh

from normalized_plot import show_normalized
from duration_plot import show_duration
from live_crypto import get_today_coin_plot
from correlation_analysis import correlation_heatmap
from histogram_analysis import returns_histogram
from moving_average import moving_average_plot
from regression_analysis import regression_profit_prediction
from rsi import rsi_plot
from bollinger_bands import bollinger_plot
from volume_analysis import volume_plot
from candlestick_chart import candlestick_plot

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="CRYPTO CURRENCY ANALYSIS", layout="wide")
st.title("CRYPTO CURRENCY ANALYSIS")
st.sidebar.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)
section = st.sidebar.radio(
    "📑 Table of Contents",
    [
        "📊 Overview",
        "📈 Market Analysis",
        "📉 Technical Indicators",
        "📊 Volume Analysis",
        "⚠️ Risk & Return",
        "🤖 Prediction"
    ]
)
st.sidebar.markdown("---")
st.sidebar.write("🔄 Live updates every 5 seconds")
st.markdown("---")

if section == "📊 Overview":
    st.subheader("📊 Overview")
    
    st.write("### 🔴 Live Price Trend")
    selected_coin = st.selectbox("Select Coin for Live Price", ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana'], key="overview_coin")
    st.write(f"Selected Coin: {selected_coin.upper()}")
    st_autorefresh(interval=3000, key="overview_live_refresh")
    fig_live = get_today_coin_plot(selected_coin)
    st.plotly_chart(fig_live, width="stretch")

elif section == "📈 Market Analysis":
    st.subheader("📈 Market Analysis")
    
    # Normalized Prices: Coin + Months
    st.write("### 📊 Normalized Prices")
    selected_coin_norm = st.selectbox("Select Coin for Normalized Prices", ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana'], key="norm_coin")
    months_norm = st.slider("Select Time Range (Months)", 1, 24, 12, key="norm_months")
    st.write(f"Coin: {selected_coin_norm.upper()} | Months: {months_norm}")
    fig_norm = show_normalized(['bitcoin','ethereum','binancecoin','cardano','solana'], months_norm*30)
    st.plotly_chart(fig_norm, width="stretch")
    
    # Duration Plot: Coin + Months
    st.write("### ⏱️ Duration Plot")
    selected_coin_dur = st.selectbox("Select Coin for Duration Plot", ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana'], key="dur_coin")
    months_dur = st.slider("Select Time Range (Months)", 1, 24, 12, key="dur_months")
    st.write(f"Coin: {selected_coin_dur.upper()} | Months: {months_dur}")
    fig_dur = show_duration(selected_coin_dur, months_dur)
    st.plotly_chart(fig_dur,width="stretch")

    # Correlation Heatmap: only Months
    st.write("### 🔗 Correlation Heatmap")
    months_corr = st.slider("Select Time Range (Months) for Correlation", 1, 24, 12, key="corr_months")
    st.write(f"Coins: bitcoin, ethereum, binancecoin, cardano, solana | Months: {months_corr}")
    fig_corr = correlation_heatmap(['bitcoin','ethereum','binancecoin','cardano','solana'], months_corr)
    st.plotly_chart(fig_corr,width="stretch")


elif section == "📉 Technical Indicators":
    st.subheader("📉 Technical Indicators")
    
    # Moving Average: Coin + Months + Window
    st.write("### 📈 Moving Average")
    selected_coin_ma = st.selectbox("Select Coin for Moving Average", ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana'], key="ma_coin")
    months_ma = st.slider("Select Time Range (Months)", 1, 24, 12, key="ma_months")
    window_ma = st.slider("Moving Average Window", 2, 30, 7, key="ma_window")
    st.write(f"Coin: {selected_coin_ma.upper()} | Months: {months_ma} | Window: {window_ma}")
    fig_ma = moving_average_plot(selected_coin_ma, months_ma, window_ma)
    st.plotly_chart(fig_ma, width="stretch")
    
    # RSI: Coin + Months
    st.write("### 📊 RSI")
    selected_coin_rsi = st.selectbox("Select Coin for RSI", ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana'], key="rsi_coin")
    months_rsi = st.slider("Select Time Range (Months)", 1, 24, 12, key="rsi_months")
    st.write(f"Coin: {selected_coin_rsi.upper()} | Months: {months_rsi}")
    fig_rsi = rsi_plot(selected_coin_rsi, months_rsi)
    st.plotly_chart(fig_rsi, width="stretch")
    
    # Bollinger Bands: Coin + Months + Window
    st.write("### 📊 Bollinger Bands")
    selected_coin_bb = st.selectbox("Select Coin for Bollinger Bands", ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana'], key="bb_coin")
    months_bb = st.slider("Select Time Range (Months)", 1, 24, 12, key="bb_months")
    window_bb = st.slider("Bollinger Window", 5, 50, 20, key="bb_window")
    st.write(f"Coin: {selected_coin_bb.upper()} | Months: {months_bb} | Window: {window_bb}")
    fig_bb = bollinger_plot(selected_coin_bb, months_bb, window_bb)
    st.plotly_chart(fig_bb, width="stretch")
    
    # Candlestick: Coin + Months
    st.write("### 📉 Candlestick Chart")
    selected_coin_candle = st.selectbox("Select Coin for Candlestick", ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana'], key="candle_coin")
    months_candle = st.slider("Select Time Range (Months)", 1, 24, 12, key="candle_months")
    st.write(f"Coin: {selected_coin_candle.upper()} | Months: {months_candle}")
    fig_candle = candlestick_plot(selected_coin_candle, months_candle)
    st.plotly_chart(fig_candle, width="stretch")


elif section == "📊 Volume Analysis":
    st.subheader("📊 Volume Analysis")
    # Volume plot needs Coin + Months
    selected_coin_vol = st.selectbox("Select Coin for Volume", ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana'], key="vol_coin")
    months_vol = st.slider("Select Time Range (Months)", 1, 24, 12, key="vol_months")
    st.write(f"Coin: {selected_coin_vol.upper()} | Months: {months_vol}")
    fig_vol = volume_plot(selected_coin_vol, months_vol)
    st.plotly_chart(fig_vol,width="stretch")


elif section == "⚠️ Risk & Return":
    st.subheader("⚠️ Risk & Return Analysis")
    # Risk & Return only needs Months
    months_rr = st.slider("Select Time Range (Months)", 1, 24, 12, key="rr_months")
    st.write(f"Coins: bitcoin, ethereum, binancecoin, cardano, solana | Months: {months_rr}")
    fig_hist, fig_scatter, stats_df = returns_histogram(['bitcoin','ethereum','binancecoin','cardano','solana'], months_rr)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_hist, width="stretch")
    with col2:
        st.plotly_chart(fig_scatter, width="stretch")
    st.subheader("📋 Statistics")
    st.dataframe(stats_df)


elif section == "🤖 Prediction":
    st.subheader("🤖 Prediction & Investment Insights")
    # Prediction only needs Months
    months_pred = st.slider("Select Time Range (Months) for Prediction", 1, 24, 12, key="pred_months")
    st.write(f"Coins: bitcoin, ethereum, binancecoin, cardano, solana | Months: {months_pred}")
    df_result, fig1, fig2, fig3 = regression_profit_prediction(['bitcoin','ethereum','binancecoin','cardano','solana'], months_pred)
    st.subheader("📊 Prediction Table")
    st.dataframe(df_result)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, width="stretch")
    with col2:
        st.plotly_chart(fig2, width="stretch")
    st.plotly_chart(fig3, width="stretch")

st.markdown("---")
st.markdown("✨ Developed for the investors who invest in cryptocurrency")