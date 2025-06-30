# Grafico candlestick con RSI e Bollinger Bands
fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close'],
    name='Candlestick'
))

# Bollinger Bands (banda alta e bassa)
fig.add_trace(go.Scatter(
    x=data.index, 
    y=data['bb_bbh'],
    line=dict(color='rgba(255,0,0,0.5)'),
    name='Bollinger High'
))

fig.add_trace(go.Scatter(
    x=data.index, 
    y=data['bb_bbl'],
    line=dict(color='rgba(0,0,255,0.5)'),
    name='Bollinger Low'
))

# RSI come secondo asse y
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['RSI'],
    line=dict(color='orange', width=1),
    name='RSI',
    yaxis='y2'
))

fig.update_layout(
    yaxis=dict(title='Price'),
    yaxis2=dict(title='RSI', overlaying='y', side='right', range=[0, 100]),
    title=f'Candlestick, Bollinger Bands & RSI for {ticker}',
    xaxis_rangeslider_visible=False,
    height=600
)

st.plotly_chart(fig)
