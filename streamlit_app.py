fig_rsi.add_trace(go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close'],
    name='Candlestick'
), row=1, col=1)

fig_rsi.add_trace(go.Scatter(
    x=data.index,
    y=data['Upper'],
    line=dict(color='rgba(255,0,0,0.5)'),
    name='Upper Band'
), row=1, col=1)

fig_rsi.add_trace(go.Scatter(
    x=data.index,
    y=data['MA20'],
    line=dict(color='rgba(0,0,255,0.5)'),
    name='MA20'
), row=1, col=1)

fig_rsi.add_trace(go.Scatter(
    x=data.index,
    y=data['Lower'],
    line=dict(color='rgba(255,0,0,0.5)'),
    name='Lower Band',
    fill='tonexty', fillcolor='rgba(255,0,0,0.1)'
), row=1, col=1)

fig_rsi.add_trace(go.Scatter(
    x=data.index,
    y=data['RSI'],
    line=dict(color='orange'),
    name='RSI'
), row=2, col=1)

fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

fig_rsi.update_yaxes(title_text="Price", row=1, col=1)
fig_rsi.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1)

fig_rsi.update_layout(height=800, showlegend=True, title_text=f"{ticker} Candlestick + RSI + Bollinger Bands")

st.plotly_chart(fig_rsi, use_container_width=True)
