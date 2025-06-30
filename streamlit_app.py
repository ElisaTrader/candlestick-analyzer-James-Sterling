import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from ta.momentum import RSIIndicator

st.set_page_config(page_title="Candlestick Analyzer", layout="wide")

st.title("Candlestick Analyzer with RSI and Bollinger Bands")

ticker = st.text_input("Enter a ticker symbol (e.g., AAPL)", value="AAPL").upper()

if ticker:
    try:
        # Download data
        data = yf.download(ticker, period="1mo", interval="1d", progress=False)

        if data.empty:
            st.error("No data found for ticker symbol. Please check the symbol and try again.")
        else:
            # Calculate RSI (14 periods)
            rsi_indicator = RSIIndicator(close=data['Close'], window=14)
            data['RSI'] = rsi_indicator.rsi()

            # Calculate Bollinger Bands (20 periods)
            window = 20
            data['MA20'] = data['Close'].rolling(window=window).mean()
            data['STD'] = data['Close'].rolling(window=window).std()
            data['Upper'] = data['MA20'] + (2 * data['STD'])
            data['Lower'] = data['MA20'] - (2 * data['STD'])

            # Drop rows with NaN
            data.dropna(inplace=True)

            # Ensure all series are 1-dimensional arrays
            index = data.index
            open_data = data['Open'].values.flatten()
            high_data = data['High'].values.flatten()
            low_data = data['Low'].values.flatten()
            close_data = data['Close'].values.flatten()
            upper_bb = data['Upper'].values.flatten()
            ma20 = data['MA20'].values.flatten()
            lower_bb = data['Lower'].values.flatten()
            rsi = data['RSI'].values.flatten()

            # Candlestick + Bollinger Bands
            fig = go.Figure()

            fig.add_trace(go.Candlestick(
                x=index,
                open=open_data,
                high=high_data,
                low=low_data,
                close=close_data,
                name='Candlestick'
            ))

            fig.add_trace(go.Scatter(
                x=index,
                y=upper_bb,
                line=dict(color='rgba(173,216,230,0.5)', width=1),
                name='Upper BB'

