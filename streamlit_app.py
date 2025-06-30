import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import numpy as np

st.title("Grafico Candlestick con RSI e Bollinger Bands")

ticker = st.text_input("Inserisci il ticker", "AAPL").upper().strip()

def calculate_rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_bollinger_bands(close, period=20, std_dev=2):
    ma = close.rolling(window=period).mean()
    std = close.rolling(window=period).std()
    upper = ma + std_dev * std
    lower = ma - std_dev * std
    return ma, upper, lower

if ticker:
    data = yf.download(ticker, period="1mo", interval="1d")

    if data.empty:
        st.error("Nessun dato trovato per il ticker inserito.")
    else:
        # Calcola RSI e Bollinger Bands
        data['RSI'] = calculate_rsi(data['Close'])
        data['MA'], data['Upper'], data['Lower'] = calculate_bollinger_bands(data['Close'])

        # Primo grafico: candlestick + Bollinger Bands
        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Candlestick'
        ))

        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Upper'],
            line=dict(color='rgba(255,0,0,0.5)', width=1),
            name='Upper BB'
        ))

        fig.add_trace(go.Scatter(
    x=data.index,
    y=data['RSI'],
    mode='lines',
    name='RSI'
))

