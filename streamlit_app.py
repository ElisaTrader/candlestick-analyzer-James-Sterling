import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import talib
import numpy as np

st.title("Candlestick Chart with RSI and Bollinger Bands")

ticker = st.text_input("Enter stock ticker", value="AAPL")

if ticker:
    data = yf.download(ticker, period="1mo", interval="1d", auto_adjust=True)
    if data.empty:
        st.error("No data found for ticker.")
    else:
        # Calcolo indicatori tecnici
        close = data['Close'].values

        rsi = talib.RSI(close, timeperiod=14)
        upper, middle, lower = talib.BBANDS(close, timeperiod=20)

        # Preparo il grafico
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
            y=upper,
            line=dict(color='rgba(255,0,0,0.5)'),
            name='Upper Bollinger Band'
        ))
        fig.add_trace(go.Scatter(
            x=data.index,
            y=middle,
            line=dict(color='rgba(0,0,255,0.5)'),
            name='Middle Bollinger Band'
        ))
        fig.add_trace(go.Scatter(
            x=data.index,
            y=lower,
            line=dict(color='rgba(255,0,0,0.5)'),
            name='Lower Bollinger Band'
        ))

        fig.update_layout(title=f'Candlestick chart for {ticker}', xaxis_title='Date', yaxis_title='Price')

        st.plotly_chart(fig)

        # Mostro RSI separatamente
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(
            x=data.index,
            y=rsi,
            line=dict(color='orange'),
            name='RSI'
        ))
        fig_rsi.update_layout(title='RSI', yaxis=dict(range=[0,100]))
        st.plotly_chart(fig_rsi)
