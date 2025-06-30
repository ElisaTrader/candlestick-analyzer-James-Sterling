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
        # Scarica dati degli ultimi 30 giorni con intervallo giornaliero
        data = yf.download(ticker, period="1mo", interval="1d", progress=False)

        if data.empty:
            st.error("No data found for ticker symbol. Please check the symbol and try again.")
        else:
            # Calcolo RSI (14 periodi) usando la libreria ta (pip install ta)
            rsi_indicator = RSIIndicator(close=data['Close'], window=14)
            data['RSI'] = rsi_indicator.rsi()

            # Calcolo Bollinger Bands (20 periodi)
            window = 20
            data['MA20'] = data['Close'].rolling(window=window).mean()
            data['STD'] = data['Close'].rolling(window=window).std()
            data['Upper'] = data['MA20'] + (2 * data['STD'])
            data['Lower'] = data['MA20'] - (2 * data['STD'])

            data.dropna(inplace=True)

            # Grafico candlestick con Bollinger Bands
            fig = go.Figure()

            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlestick'
            ))

            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Upper'],
                line=dict(color='rgba(173,216,230,0.5)', width=1),
                name='Upper BB'
            ))

            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['MA20'],
                line=dict(color='rgba(0,0,255,0.8)', width=1),
                name='MA20'
            ))

            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Lower'],
                line=dict(color='rgba(173,216,230,0.5)', width=1),
                name='Lower BB'
            ))

            fig.update_layout(title=f"Candlestick Chart with Bollinger Bands for {ticker}",
                              xaxis_title="Date",
                              yaxis_title="Price (USD)",
                              xaxis_rangeslider_visible=False)

            st.plotly_chart(fig, use_container_width=True)

            # Grafico RSI
            fig_rsi = go.Figure()
            fig_rsi.add_trace(go.Scatter(
                x=data.index,
                y=data['RSI'],
                line=dict(color='orange', width=2),
                name='RSI'
            ))

            fig_rsi.update_layout(title='RSI (14 periods)',
                                  yaxis=dict(range=[0, 100]),
                                  xaxis_title="Date",
                                  yaxis_title="RSI Value",
                                  shapes=[
                                      dict(type='line', y0=70, y1=70, x0=data.index[0], x1=data.index[-1], line=dict(color='red', dash='dash')),
                                      dict(type='line', y0=30, y1=30, x0=data.index[0], x1=data.index[-1], line=dict(color='green', dash='dash')),
                                  ])

            st.plotly_chart(fig_rsi, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
