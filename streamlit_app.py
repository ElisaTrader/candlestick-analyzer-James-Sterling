import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Funzione per calcolare RSI
def compute_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Funzione per calcolare Bollinger Bands
def compute_bollinger_bands(data, window=20, no_of_std=2):
    rolling_mean = data['Close'].rolling(window).mean()
    rolling_std = data['Close'].rolling(window).std()
    upper_band = rolling_mean + (rolling_std * no_of_std)
    lower_band = rolling_mean - (rolling_std * no_of_std)
    return rolling_mean, upper_band, lower_band

# Streamlit UI
st.title("Candlestick Chart with RSI and Bollinger Bands")

ticker = st.text_input("Enter ticker symbol:", value="AAPL")

if ticker:
    data = yf.download(ticker, period="1mo", interval="1d")
    
    if data.empty:
        st.error("No data found for ticker symbol. Please check the symbol and try again.")
    else:
        # Calcoli indicatori
        data['RSI'] = compute_rsi(data)
        data['MA'], data['Upper BB'], data['Lower BB'] = compute_bollinger_bands(data)

        # Grafico candlestick
        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=data.in)

