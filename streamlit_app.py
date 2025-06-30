fig = make_subplots(
    rows=2, cols=1, shared_xaxes=True,
    vertical_spacing=0.1,
    row_heights=[0.7, 0.3],
    specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
)

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

fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data['RSI'],
        line=dict(color='orange'),
        name='RSI'
    ),
    row=2, col=1
)
