import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.title("Test Candlestick Puro")

ticker = st.text_input("Inserisci ticker:", "AAPL")

if ticker:
    data = yf.download(ticker, period="3mo", interval="1d")
    
    if data.empty:
        st.error("Nessun dato trovato.")
    else:
        data = data.dropna(subset=['Open', 'High', 'Low', 'Close'])
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data.index)
        
        st.write(data.tail(10))
        
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        )])
        
        fig.update_layout(title=f"Candlestick {ticker.upper()}", xaxis_rangeslider_visible=False)
        
        st.plotly_chart(fig, use_container_width=True)
