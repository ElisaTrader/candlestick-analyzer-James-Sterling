import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import numpy as np

# Funzione semplice per calcolare RSI
def compute_rsi(data, window=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Funzione per calcolare Bollinger Bands
def compute_bollinger_bands(data, window=20, num_std=2):
    rolling_mean = data.rolling(window=window).mean()
    rolling_std = data.rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return rolling_mean, upper_band, lower_band

st.title("Candlestick Chart con RSI e Bollinger Bands")

# Input ticker
ticker = st.text_input("Inserisci il ticker del titolo (es: AAPL, MSFT)", value="AAPL")

if ticker:
    data = yf.download(ticker, period="1mo", interval="1d", auto_adjust=True)

    if data.empty:
        st.error("Nessun dato trovato per questo ticker.")
    else:
        data = data.dropna()

        # Calcola RSI
        data['RSI'] = compute_rsi(data['Close'])

        # Calcola Bollinger Bands
        data['MA20'], data['BB_upper'], data['BB_lower'] = compute_bollinger_bands(data['Close'])

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
            y=data['BB_upper'],
            line=dict(color='rgba(173,216,230,0.5)'),
            name='Bollinger Upper'
        ))

        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['BB_lower'],
            line=dict(color='rgba(173,216,230,0.5)'),
            fill='tonexty',
            fillcolor='rgba(173,216,230,0.2)',
            name='Bollinger Lower'
        ))

        fig.update_layout(title=f'{ticker} Candlestick con Bollinger Bands', xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # Grafico RSI
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(
            x=data.index,
            y=data['RSI'],
            line=dict(color='orange'),
            name='RSI'
        ))

        fig_rsi.update_layout(
            title='RSI',
            yaxis=dict(range=[0, 100]),
            xaxis=dict(range=[data.index.min(), data.index.max()])
        )

        st.plotly_chart(fig_rsi, use_container_width=True)
