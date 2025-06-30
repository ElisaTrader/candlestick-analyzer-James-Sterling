import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Candlestick + RSI + Bollinger Bands (no TA-Lib)", layout="wide")

st.title("Candlestick Chart with RSI and Bollinger Bands (No TA-Lib)")

ticker = st.text_input("Enter ticker symbol (e.g. AAPL)", "AAPL")

@st.cache_data(show_spinner=False)
def load_data(ticker):
    try:
        data = yf.download(ticker, period="3mo", interval="1d", progress=False)
        if data.empty:
            return None
        return data
    except Exception:
        return None

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_bollinger_bands(series, period=20, std_dev=2):
    sma = series.rolling(window=period).mean()
    rstd = series.rolling(window=period).std()
    upper_band = sma + std_dev * rstd
    lower_band = sma - std_dev * rstd
    return upper_band, sma, lower_band

if ticker:
    data = load_data(ticker)
    if data is None:
        st.error("No data found for ticker: " + ticker)
    else:
        data['RSI'] = calculate_rsi(data['Close'])
        data['BB_upper'], data['BB_middle'], data['BB_lower'] = calculate_bollinger_bands(data['Close'])

        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            cl
