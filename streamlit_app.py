import streamlit as st
import yfinance as yf
import talib
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

st.title("Candlestick Analyzer con RSI e Bollinger Bands")

ticker = st.text_input("Inserisci il simbolo del ticker (es. AAPL):", "AAPL")

if ticker:
    data = yf.download(ticker, period="1mo", interval="1d")

    if data.empty:
        st.error("Nessun dato trovato per questo ticker.")
    else:
        data.dropna(inplace=True)

        # Calcolo indicatori
        data['RSI'] = talib.RSI(data['Close'], timeperiod=14)
        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['STD'] = data['Close'].rolling(window=20).std()
        data['Upper'] = data['MA20'] + (2 * data['STD'])
        data['Lower'] = data['MA20'] - (2 * data['STD'])

        # Creazione grafico con subplot
        fig = make_subplots(
            rows=2, cols=1, shared_xaxes=True,
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3],
            specs=[[{}], [{}]]
        )

        # Candlestick + Bollinger Bands
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlestick'
            ),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['Upper'],
                line=dict(color='rgba(255,0,0,0.5)'),
                name='Upper Band'
            ),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['MA20'],
                line=dict(color='rgba(0,0,255,0.5)'),
                name='Middle Band (MA20)'
            ),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['Lower'],
                fill='tonexty',
                fillcolor='rgba(255,0,0,0.1)',
                line=dict(color='rgba(255,0,0,0.5)'),
                name='Lower Band'
            ),
            row=1, col=1
        )

        # RSI subplot
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['RSI'],
                line=dict(color='orange'),
                name='RSI'
            ),
            row=2, col=1
        )
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1)

        fig.update_layout(
            height=700,
            showlegend=True,
            title=f"Analisi candlestick di {ticker.upper()} con RSI e Bollinger Bands"
        )

        st.plotly_chart(fig, use_container_width=True)
