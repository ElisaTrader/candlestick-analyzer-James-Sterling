import streamlit as st
import yfinance as yf
import ta
import plotly.graph_objects as go

st.title("Candlestick Analyzer con RSI e Bollinger Bands")

# Input ticker da utente
ticker = st.text_input("Inserisci il ticker (esempio: AAPL):", "AAPL")

if ticker:
    # Scarica dati storici (1 mese giornaliero)
    data = yf.download(ticker, period="1mo", interval="1d")

    if not data.empty:
        # Assicurati che 'Close' sia Series monodimensionale
        close_prices = data['Close']
        
        # Calcola RSI
        rsi_indicator = ta.momentum.RSIIndicator(close_prices)
        data['RSI'] = rsi_indicator.rsi()

        # Calcola Bollinger Bands
        bb_indicator = ta.volatility.BollingerBands(close_prices)
        data['bb_bbh'] = bb_indicator.bollinger_hband()
        data['bb_bbl'] = bb_indicator.bollinger_lband()

        # Crea grafico candlestick con Plotly
        fig = go.Figure()

        # Candlestick
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Candlestick'
        ))

        # Bollinger Bands - upper band
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['bb_bbh'],
            line=dict(color='rgba(255,0,0,0.5)'),
            name='Bollinger High'
        ))

        # Bollinger Bands - lower band
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['bb_bbl'],
            line=dict(color='rgba(0,0,255,0.5)'),
            name='Bollinger Low'
        ))

        # RSI su asse y2
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['RSI'],
            line=dict(color='orange', width=1),
            name='RSI',
            yaxis='y2'
        ))

        fig.update_layout(
            title=f'Candlestick, Bollinger Bands & RSI per {ticker.upper()}',
            yaxis=dict(title='Price'),
            yaxis2=dict(title='RSI', overlaying='y', side='right', range=[0, 100]),
            xaxis_rangeslider_visible=False,
            height=600
        )

        st.plotly_chart(fig)
    else:
        st.warning("Nessun dato trovato per questo ticker. Prova con un altro.")
else:
    st.info("Inserisci un ticker per iniziare l'analisi.")
