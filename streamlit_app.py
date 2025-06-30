import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta  # libreria tecnica

st.title("Candlestick Trading Analyzer")

ticker = st.text_input("Enter ticker symbol", "AAPL")

if ticker:
    data = yf.download(ticker, period="60d", interval="1d")
    if not data.empty:
        # Calcolo RSI (default window 14)
        rsi_indicator = ta.momentum.RSIIndicator(close=data['Close'], window=14)
        data['RSI'] = rsi_indicator.rsi()

        # Calcolo MACD
        macd_indicator = ta.trend.MACD(close=data['Close'])
        data['MACD'] = macd_indicator.macd()
        data['MACD_signal'] = macd_indicator.macd_signal()
        data['MACD_diff'] = macd_indicator.macd_diff()

        # Calcolo Bollinger Bands
        bb_indicator = ta.volatility.BollingerBands(close=data['Close'], window=20, window_dev=2)
        data['bb_bbm'] = bb_indicator.bollinger_mavg()
        data['bb_bbh'] = bb_indicator.bollinger_hband()
        data['bb_bbl'] = bb_indicator.bollinger_lband()

        # Grafico candlestick con RSI e Bollinger Bands
        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Candlestick'
        ))

        # Bollinger Bands (banda alta e bassa)
        fig.add_trace(go.Scatter(
            x=data.index, y=data['bb_bbh'],
            line=dict(color='rgba(255,0,0,0.5)'),
