
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import talib
from datetime import datetime

st.set_page_config(page_title="Candlestick Analyzer", layout="wide")

st.title("📊 Candlestick Trading Analyzer")
st.markdown("Carica un file CSV oppure inserisci un simbolo per scaricare i dati dal mercato.")

# Funzione per scaricare i dati da Yahoo Finance
def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data.reset_index(inplace=True)
    return data

# Sezione upload o download
upload_method = st.radio("📥 Seleziona input dati:", ["Carica CSV", "Inserisci simbolo (Yahoo Finance)"])

if upload_method == "Carica CSV":
    uploaded_file = st.file_uploader("Carica il tuo file CSV (con colonne: Date, Open, High, Low, Close)", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
else:
    ticker = st.text_input("Inserisci simbolo (es. AAPL, TSLA, BTC-USD):", value="AAPL")
    start_date = st.date_input("Data inizio", datetime(2023, 1, 1))
    end_date = st.date_input("Data fine", datetime.today())
    if ticker:
        df = load_data(ticker, start_date, end_date)

# Se ci sono dati disponibili, analizziamoli
if 'df' in locals():
    st.subheader("📈 Grafico Candlestick + Indicatori")
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Indicatori tecnici
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df['RSI'] = talib.RSI(df['Close'])
    macd, signal, _ = talib.MACD(df['Close'])
    df['MACD'] = macd
    df['Signal'] = signal

    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="Candlestick")])

    fig.add_trace(go.Scatter(x=df.index, y=df['SMA20'], mode='lines', name='SMA20', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA50'], mode='lines', name='SMA50', line=dict(color='orange')))

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔍 Pattern Candlestick Rilevati")

    patterns = {
        "Hammer": talib.CDLHAMMER,
        "Engulfing": talib.CDLENGULFING,
        "Doji": talib.CDLDOJI,
        "Hanging Man": talib.CDLHANGINGMAN,
        "Shooting Star": talib.CDLSHOOTINGSTAR
    }

    for name, func in patterns.items():
        result = func(df['Open'], df['High'], df['Low'], df['Close'])
        matches = df[result != 0]
        st.markdown(f"**{name}**: trovati {len(matches)} pattern")
        if not matches.empty:
            st.dataframe(matches[['Open', 'High', 'Low', 'Close']].tail(5))

    st.subheader("🧠 Commenti automatici")
    latest_rsi = df['RSI'].iloc[-1]
    if latest_rsi < 30:
        st.warning("🔻 RSI < 30: condizione di ipervenduto, possibile rimbalzo.")
    elif latest_rsi > 70:
        st.warning("🔺 RSI > 70: condizione di ipercomprato, possibile inversione.")
    else:
        st.info("🔄 RSI neutro, nessun segnale forte.")

    macd_cross = df['MACD'].iloc[-1] - df['Signal'].iloc[-1]
    if macd_cross > 0:
        st.success("✅ MACD sopra la Signal Line: trend positivo.")
    else:
        st.error("⚠️ MACD sotto la Signal Line: possibile debolezza.")
