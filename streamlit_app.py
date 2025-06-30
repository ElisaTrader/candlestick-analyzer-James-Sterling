import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.title("Candlestick Chart with RSI and Bollinger Bands")

ticker = st.text_input("Enter ticker symbol (e.g. AAPL):", value="AAPL")

if ticker:
    data = yf.download(ticker, period="1mo", interval="1d")
    
    if data.empty:
        st.error("Nessun dato trovato per questo ticker. Prova un altro simbolo.")
        st.stop()

    st.write("Dati scaricati (prime 5 righe):")
    st.write(data.head())

    # Calcolo RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi

    # Calcolo Bollinger Bands
    window = 20
    data['MA20'] = data['Close'].rolling(window=window).mean()
    data['STD']
