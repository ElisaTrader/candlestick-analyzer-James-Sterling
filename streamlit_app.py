import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.title("Candlestick Analyzer con Debug")

ticker = st.text_input("Inserisci ticker:", "AAPL")

if ticker:
    # Scarico 6 mesi per avere dati più consistenti
    data = yf.download(ticker, period="6mo", interval="1d")
    
    st.write("Ultime righe dati scaricati:")
    st.write(data.tail(10))
    
    # Rimuovo righe con NaN nelle colonne essenziali
    data = data.dropna(subset=['Open', 'High', 'Low', 'Close'])
    
    if data.empty:
        st.error("Dati insufficienti o non trovati per il ticker.")
    else:
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data.index)
        
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        )])
        
        fig.update_layout(title=f"Candlestick per {ticker.upper()}", xaxis_rangeslider_visible=False)
        
        st.plotly_chart(fig, use_container_width=True)

