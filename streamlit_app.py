import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta  # technical analysis library

st.title("Candlestick Chart with RSI and Bollinger Bands")

ticker = st.text_input("Enter stock ticker", value="AAPL")

if ticker:
    data = yf.download(ticker, period="1mo", interval="1d", auto_adjust=True)
    if data.empty:
        st.error("No data found for ticker.")
    else:
        # Calcolo indicatori con 'ta'
        data['rsi'] = ta.momentum.RSIIndicator(close=data['Close'], window=14).rsi()
        bb_indicator = ta.volatility.BollingerBands(close=data['Close'], window=20, window_dev=2)
        data['bb_high'] = bb_indicator.bollinger_hband()
        data['bb_mid'] = bb_indicator.bollinger_mavg()
        data['bb_low'] = bb_indicator.bollinger_lband()

        # Grafico candlestick
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
            y=data['bb_high'],
            line=dict(color='rgba(255,0,0,0.5)'),
            name='Upper Bollinger Band'
        ))
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['bb_mid'],
            line=dict(color='rgba(0,0,255,0.5)'),
            name='Middle Bollinger Band'
        ))
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['bb_low'],
            line=dict(color='rgba(255,0,0,0.5)'),
            name='Lower Bollinger Band'
        ))

        fig.update_layout(title=f'Candlestick chart for {ticker}', xaxis_title='Date', yaxis_title='Price')
        st.plotly_chart(fig)

        # RSI separato
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(
            x=data.index,
            y=data['rsi'],
            line=dict(color='orange'),
            name='RSI'
        ))
        fig_rsi.update_layout(title='RSI', yaxis=dict(range=[0]()
