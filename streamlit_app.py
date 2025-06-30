import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.title("Candlestick Chart Basic Demo")

ticker = st.text_input("Enter ticker symbol:", "AAPL").upper()

if ticker:
    data = yf.download(ticker, period="1mo", interval="1d", progress=False)
    if data.empty:
        st.error("No data found for ticker: " + ticker)
    else:
        st.write(data)  # debug: mostra dati scaricati
        
        data.index = data.index.to_pydatetime()  # assicura datetime
        
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        )])
        st.plotly_chart(fig, use_container_width=True)
