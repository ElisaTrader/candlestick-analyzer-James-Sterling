import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.title("Candlestick Analyzer con debug colonne")

ticker = st.text_input("Inserisci ticker:", "AAPL")

if ticker:
    data = yf.download(ticker, period="6mo", interval="1d")
    st.write("Colonne disponibili:", data.columns.tolist())
    st.write("Dati ultimi 5:", data.tail())

    # Controllo se ci sono le colonne necessarie prima di procedere
    required_cols = ['Open', 'High', 'Low', 'Close']
    if all(col in data.columns for col in required_cols):
        data = data.dropna(subset=required_cols)

        if data.empty:
            st.error("Dati insufficienti dopo aver rimosso NaN.")
        else:
            if not isinstance(data.index, pd.DatetimeIndex):
                data.index = pd.to_datetime(data.index)

            fig = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close']
            )])

            fig.update_layout(title=f"Candlestick per {ticker.upper()}", xaxis_rangeslider_visible=False)

            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"Dati scaricati non contengono le colonne essenziali: {required_cols}")
