import streamlit as st
import yfinance as yf
import talib
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

st.title("Candlestick Analyzer con RSI e Bollinger Bands")

ticker = st.text_input("Inserisci il ticker del titolo (es: AAPL, MSFT):", "AAPL")

if ticker:
    try:
        # Scarica dati ultimi 30 giorni giornalieri
        data = yf.download(ticker, period="1mo", interval="1d")
        if data.empty:
            st.error("Nessun dato trovato per questo ticker.")
        else:
            # Calcolo indicatori TA con TA-Lib (assicurati che sia installato)
            close = data['Close'].values
            data['RSI'] = talib.RSI(close, timeperiod=14)
            data['MA20'] = talib.SMA(close, timeperiod=20)
            upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
            data['Upper'] = upper
            data['MA20'] = middle
            data['Lower'] = lower

            data = data.dropna()  # rimuove righe con NaN

            # Creazione grafico a due righe: candlestick + Bollinger Bands sopra, RSI sotto
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                vertical_spacing=0.1,
                                row_heights=[0.7, 0.3],
                                specs=[[{"secondary_y": False}], [{"secondary_y": False}]])

            # Candlestick + Bollinger Bands
            fig.add_trace(go.Candlestick(
                x=dat
