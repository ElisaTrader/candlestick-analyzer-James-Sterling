import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Se non hai TA-Lib installato, puoi usare questo semplice calcolo RSI alternativo
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calcolo Bollinger Bands
def calculate_bollinger_bands(series, window=20, no_of_std=2):
    ma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    upper_band = ma + (std * no_of_std)
    lower_band = ma - (std * no_of_std)
    return ma, upper_band, lower_band

st.title("Candlestick Chart with RSI and Bollinger Bands")

ticker = st.text_input("Enter ticker symbol", "AAPL").upper()

if ticker:
    data = yf.download(ticker, period="1mo", interval="1d", progress=False)
    
    if data.empty:
        st.error("No data found for ticker symbol. Please try another one.")
    else:
        # Calcolo indicatori
        data['RSI'] = calculate_rsi(data['Close'])
        data['MA'], data['Upper'], data['Lower'] = calculate_bollinger_bands(data['Close'])
        
        # Grafico candlestick con Bollinger Bands

