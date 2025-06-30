import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta

st.title("Candlestick Analyzer con RSI e Bollinger Bands")

# Input ticker da utente
ticker = st.text_input("Inserisci il ticker (esempio: AAPL):", "AAPL")

# Scarica dati storici
data = yf.download(ticker, period="1mo", interval="1d")

# Calcola indicatori
data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()
bb_indicator = ta.volatility.BollingerBands(data['Close'])
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

fig.add_trace(go.Scatter(
    x=data.index,
    y=data['bb_bbh'],
    line=dict(color='rgba(255,0,0,0.5)'),
    name='Bollinger High'
))

fig.add_trace(go.Scatter(
    x=data.index,
    y=data['bb_bbl'],
    line=dict(color='rgba(0,0,255,0.5)'),
    name='Bollinger Low'
))

fig.add_trace(go.Scatter(
    x=data.index,
    y=data['RSI'],
    line=dict(color='orange', width=1),
    name='RSI',
    yaxis='y2'
))

fig.update_layout(
    yaxis=dict(title='Price'),
    yaxis2=dict(title='RSI', overlaying='y', side='right', range=[0, 100]),
    title=f'Candlestick, Bollinger Bands & RSI for {ticker}',
    xaxis_rangeslider_visible=False,
    height=600
)

st.plotly_chart(fig)
