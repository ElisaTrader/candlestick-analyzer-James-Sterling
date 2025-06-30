import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots  # <-- Import corretto

st.title("Candlestick Chart with RSI & Bollinger Bands")

ticker = st.text_input("Ticker", "AAPL").upper()
period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y"], index=0)
interval = st.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)

if ticker:
    data = yf.download(ticker, period=period, interval=interval, progress=False)

    if data.empty:
        st.error("No data found for ticker")
    else:
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel(1)

        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['STD'] = data['Close'].rolling(window=20).std()
        data['Upper'] = data['MA20'] + (2 * data['STD'])
        data['Lower'] = data['MA20'] - (2 * data['STD'])

        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))

        data.dropna(inplace=True)

        fig_rsi = make_subplots(
            rows=2, cols=1, shared_xaxes=True,
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3]
        )

        fig_rsi.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Candlestick'
        ), row=1, col=1)

        fig_rsi.add_trace(go.Scatter(
            x=data.index,
            y=data['Upper'],
            line=dict(color='rgba(255,0,0,0.5)'),
            name='Upper Band'
        ), row=1, col=1)

        fig_rsi.add_trace(go.Scatter(
            x=data.index,
            y=data['MA20'],
            line=dict(color='rgba(0,0,255,0.5)'),
            name='MA20'
        ), row=1, col=1)

        fig_rsi.add_trace(go.Scatter(
            x=data.index,
            y=data['Lower'],
            line=dict(color='rgba(255,0,0,0.5)'),
            name='Lower Band',
            fill='tonexty', fillcolor='rgba(255,0,0,0.1)'
        ), row=1, col=1)

        fig_rsi.add_trace(go.Scatter(
            x=data.index,
