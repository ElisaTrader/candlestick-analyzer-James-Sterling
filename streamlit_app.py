import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title("Candlestick Analyzer con RSI e Bollinger Bands (senza talib)")

ticker = st.text_input("Inserisci il simbolo del ticker (es. AAPL):", "AAPL")

def compute_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

if ticker:
    # Scarico più dati (3 mesi)
    data = yf.download(ticker, period="3mo", interval="1d")
    
    if data.empty:
        st.error("Nessun dato trovato per questo ticker.")
    else:
        # Assicurati che l'indice sia datetime
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data.index)
        
        data.dropna(inplace=True)
        st.write("Anteprima dati:", data.tail(10))  # Per debug visivo
        
        # Calcolo RSI manuale
        data['RSI'] = compute_rsi(data['Close'], window=14)
        
        # Calcolo Bollinger Bands manuale
        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['STD'] = data['Close'].rolling(window=20).std()
        data['Upper'] = data['MA20'] + (2 * data['STD'])
        data['Lower'] = data['MA20'] - (2 * data['STD'])
        
        # Subplots: prima candlestick + bande, seconda RSI
        fig = make_subplots(
            rows=2, cols=1, shared_xaxes=True,
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3],
            specs=[[{"type": "candlestick"}], [{}]]
        )
        
        # Candlestick
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
        
        # Bande di Bollinger solo se non sono tutte NaN
        if not data['Upper'].isna().all():
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
        
        # RSI subplot (se non tutto NaN)
        if not data['RSI'].isna().all():
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['RSI'],
                    line=dict(color='orange'),
                    name='RSI'
                ),
                row=2, col=1
            )
            fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1)
        else:
            fig.update_yaxes(showticklabels=False, row=2, col=1)
        
        fig.update_yaxes(title_text="Price", row=1, col=1)
        
        fig.update_layout(
            height=700,
            showlegend=True,
            title=f"Analisi candlestick di {ticker.upper()} con RSI e Bollinger Bands"
        )
        
        st.plotly_chart(fig, use_container_width=True)
