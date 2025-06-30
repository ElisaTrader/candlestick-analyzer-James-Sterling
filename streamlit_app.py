import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.title("Candlestick Chart with RSI & Bollinger Bands")

# Input interattivi
ticker = st.text_input("Ticker", "AAPL").upper()
period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y"], index=0)
interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)

if ticker:
    data = yf.download(ticker, period=period, interval=interval, progress=False)

    if data.empty:
        st.error("No data found for ticker")
    else:
        # Sistema colonne se MultiIndex
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel(1)

        # Calcolo Bollinger Bands (20 giorni, 2 deviazioni standard)
        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['STD'] = data['Close'].rolling(window=20).std()
        data['Upper'] = data['MA20'] + (2 * data['STD'])
        data['Lower'] = data['MA20'] - (2 * data['STD'])

        # Calcolo RSI 14 periodi
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))

        data.dropna(inplace=True)

        # Grafico candlestick con Bollinger Bands
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
            line=dict(color='rgba(255,0,0,0.5)'),
            name='Upper Band'
        ))

        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['MA20'],
            line=dict(color='rgba(0,0,255,0.5)'),
            name='MA20'
        ))

        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Lower'],
            line=dict(color='rgba(255,0,0,0.5)'),
            name='Lower Band',
            fill='tonexty', fillcolor='rgba(255,0,0,0.1)'
        ))

        # Crea un sottografo per RSI
        from plotly.subplots import make_subplots
        fig_rsi = make_subp
