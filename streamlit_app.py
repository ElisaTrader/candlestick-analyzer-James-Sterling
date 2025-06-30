import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.title("Test Grafico Candlestick")

ticker = st.text_input("Inserisci il ticker", "AAPL")

if ticker:
    data = yf.download(ticker, period="1mo", interval="1d")

    if data.empty:
        st.write("Nessun dato trovato per questo ticker.")
    else:
        st.write(data)  # Debug: mostra i dati scaricati

        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Candlestick'
        ))

        fig.update_layout(title=f"Candlestick Chart - {ticker}",
                          xaxis_title="Date",
                          yaxis_title="Price")

        st.plotly_chart(fig)
