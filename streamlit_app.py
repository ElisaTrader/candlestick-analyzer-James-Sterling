import streamlit as st
import yfinance as yf
import pandas as pd
import talib
import plotly.graph_objects as go

st.set_page_config(page_title="Candlestick + RSI + Bollinger Bands", layout="wide")

st.title("Candlestick Chart con RSI e Bollinger Bands")

ticker = st.text_input("Inserisci il simbolo ticker (es. AAPL)", "AAPL")

@st.cache_data(show_spinner=False)
def load_data(ticker):
    try:
        # Scarico 3 mesi dati giornalieri
        data = yf.download(ticker, period="3mo", interval="1d", progress=False)
        if data.empty:
            return None
        return data
    except Exception:
        return None

if ticker:
    data = load_data(ticker)
    if data is None:
        st.error(f"Nessun dato trovato per il ticker: {ticker}")
    else:
        # Calcolo indicatori con TA-Lib
        data['RSI'] = talib.RSI(data['Close'], timeperiod=14)
        upper, middle, lower = talib.BBANDS(data['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        data['BB_upper'] = upper
        data['BB_middle'] = middle
        data['BB_lower'] = lower

        # --- GRAFICO CANDLESTICK ---
        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Candlestick'
        ))

        # Bollinger Bands
        fig.add_trace(go.Scatter(
            x=data.index, y=data['BB_upper'],
            line=dict(color='rgba(255, 0, 0, 0.5)', width=1),
            name='BB Upper'
        ))
        fig.add_trace(go.Scatter(
            x=data.index, y=data['BB_middle'],
            line=dict(color='rgba(0, 0, 255, 0.5)', width=1),
            name='BB Middle'
        ))
        fig.add_trace(go.Scatter(
            x=data.index, y=data['BB_lower'],
            line=dict(color='rgba(255, 0, 0, 0.5)', width=1),
            name='BB Lower',
            fill='tonexty',
            fillcolor='rgba(255, 0, 0, 0.1)'
        ))

        fig.update_layout(
            title=f"Candlestick Chart per {ticker}",
            xaxis_title='Data',
            yaxis_title='Prezzo',
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        # --- GRAFICO RSI ---
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(
            x=data.index,
            y=data['RSI'],
            line=dict(color='orange', width=2),
            name='RSI'
        ))
        fig_rsi.update_layout(
            title="Indice di Forza Relativa (RSI)",
            yaxis=dict(range=[0, 100]),
            template='plotly_dark',
            height=300
        )
        st.plotly_chart(fig_rsi, use_container_width=True)

        # Mostro ultimi dati
        st.subheader("Ultimi dati")
        st.dataframe(data.tail(5))

