import pandas as pd
import plotly.graph_objects as go

df_unemp = pd.read_csv('../data/bls_unemployment_rate.csv')
df_import = pd.read_csv('../data/bls_import_prices.csv')
df_export = pd.read_csv('../data/bls_export_prices.csv')

for df in [df_unemp, df_import, df_export]:
    df['Date'] = pd.to_datetime(df['Date'])

fig = go.Figure()

# Unemployment
fig.add_trace(go.Scatter(
    x=df_unemp['Date'],
    y=df_unemp['Total'],
    mode='lines',
    name='Unemployment rate',
    visible=True,
    line=dict(color='#F73351', width=2),
    hovertemplate='Date: %{x|%b %Y}<br>Unemployment rate: %{y:.1f}%<extra></extra>',
    hoverlabel=dict(
        bgcolor='white',
        font_color='black',
        bordercolor='black',
        font_size=14
    )
))

# Import prices
fig.add_trace(go.Scatter(
    x=df_import['Date'],
    y=df_import['All imports'],
    mode='lines',
    name='Import prices',
    visible=False,
    line=dict(color='#0072B2', width=2),
    hovertemplate='Date: %{x|%b %Y}<br>All imports: %{y:.1f}%<extra></extra>',
    hoverlabel=dict(
        bgcolor='white',
        font_color='black',
        bordercolor='black',
        font_size=14
    )
))

# Export prices
fig.add_trace(go.Scatter(
    x=df_export['Date'],
    y=df_export['All exports'],
    mode='lines',
    name='Export prices',
    visible=False,
    line=dict(color='#009E73', width=2),
    hovertemplate='Date: %{x|%b %Y}<br>All exports: %{y:.1f}%<extra></extra>',
    hoverlabel=dict(
        bgcolor='white',
        font_color='black',
        bordercolor='black',
        font_size=14
    )
))

fig.update_layout(
    updatemenus=[dict(
        type="dropdown",
        active=0,
        buttons=list([
            dict(label="Unemployment rate",
                 method="update",
                 args=[{"visible": [True, False, False]},
                       {"yaxis.title.text": "Unemployment rate [%]"}]),

            dict(label="Import prices",
                 method="update",
                 args=[{"visible": [False, True, False]},
                       {"yaxis.title.text": "Import price change [%]"}]),

            dict(label="Export prices",
                 method="update",
                 args=[{"visible": [False, False, True]},
                       {"yaxis.title.text": "Export price change [%]"}]),
        ]),
        x=0,
        xanchor='left',
        y=1.15,
        yanchor='top'
    )]
)

fig.update_layout(
    title=dict(
        text="Economic indicators in the United States (2016–2025)",
        font=dict(size=24, color='black', weight='bold'),
        x=0.9
    ),
    xaxis=dict(
        title='Date',
        title_standoff=20,
        tickfont=dict(size=16),
        tickformat='%b-%Y',
        tickangle=-30,
        dtick="M6",
        ticks='outside',
        title_font=dict(size=22, color='black', weight='bold'),
        gridcolor='#E8E8E8',
        linecolor='black',
    ),
    yaxis=dict(
        title='Unemployment rate [%]',
        title_standoff=30,
        tickfont=dict(size=16),
        title_font=dict(size=22, color='black', weight='bold'),
        ticks='outside',
        gridcolor='#E8E8E8',
        linecolor='black',
    ),
    width=1200,
    height=700,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=150, r=50, t=100, b=80),
)

#fig.show()
fig.write_html("../plots/economic_indicators.html")