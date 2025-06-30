import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.title("Candlestick Chart with RSI and Bollinger Bands")

ticker = st.text_input("Enter ticker symbol (e.g. AAPL):", value="AAPL")

if ticker:
    # Scarica dati con auto_adjust=True
    data = yf.download(ticker, period="1mo", interval="1d", auto_adjust=True)

    if data.empty:
        st.error("Nessun dato trovato per questo ticker. Prova un altro simbolo.")
        st.stop()

    # Se le colonne sono MultiIndex, appiattiscile
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [' '.join(col).strip() for col in data.columns.values]

    st.write("Dati scaricati (prime 5 righe):")
    st.write(data.head())

    # Per sicurezza, usa solo colonne essenziali (Close, Open, High, Low)
    required_cols = ['Open', 'High', 'Low', 'Close']
    for col in required_cols:
        if col not in data.columns:
            st.error(f"Colonna '{col}' mancante nei dati scaricati.")
            st.stop()

    # Calcolo RSI (14 periodi)
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi

    # Calcolo Bollinger Bands (20 periodi)
    window = 20
    data['MA20'] = data['Close'].rolling(window=window).mean()
    data['STD'] = data['Close'].rolling(window=window).std()
    data['Upper'] = data['MA]()
