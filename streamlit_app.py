import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.title("Candlestick Chart Basic Demo")

ticker = st.text_input("Enter ticker symbol:", "AAPL").upper()

if ticker:
    data = yf.download(ticker, period="1mo", interval="1d", progress=False)

    # DEBUG: vedere le colonne
    st.write("Columns before fix:", data.columns)

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
    
    st.write("Columns after fix:", data.columns)

    if data.empty:
        st.error("No data found for ticker: " + ticker)
    else:
        st.write(data)
        st.write("NaN presenti nelle colonne:", data.isna().sum())

        data.index = pd.to_datetime(data.index)

        data['Open'] = pd.to_numeric(data['Open'], errors='coerce')
        data['High'] = pd.to_numeric(data['High'], errors='coerce')
        data['Low'] = pd.to_numeric(data['Low'], errors='coerce')
        data['Close'] = pd.to_numeric(data['Close'], errors='coerce')

        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        )])

        fig.update_layout(title=f"Candlestick chart for {ticker}")
        st.plotly_chart(fig, use_container_width=True)
