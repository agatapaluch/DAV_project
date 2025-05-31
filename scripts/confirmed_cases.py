import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

df = pd.read_csv('../data/weekly-confirmed-covid-19-cases-per-million-people.csv')
df['Day'] = pd.to_datetime(df['Day'])

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['Day'],
    y=df['Weekly cases per million people'],
    mode='lines',
    line=dict(color='#F73351', width=2),
    hovertemplate='Date: %{x|%b %d, %Y}<br>Weekly confirmed cases per million: %{y:,.0f}<extra></extra>',
    hoverlabel=dict(
        bgcolor='white',
        font_color='black',
        bordercolor='black',
        font_size=14
    )
))

waves = [
    {'name': 'First wave', 'start': '2020-03-01', 'end': '2020-05-31', 'color': 'rgba(128,165,128,0.2)'},
    {'name': 'Second wave', 'start': '2020-10-01', 'end': '2021-02-28', 'color': 'rgba(255,165,0,0.2)'},
    {'name': 'Delta variant', 'start': '2021-06-01', 'end': '2021-10-31', 'color': 'rgba(255,255,0,0.2)'},
    {'name': 'Omicron variant', 'start': '2021-12-01', 'end': '2022-03-15', 'color': 'rgba(255,0,0,0.2)'}
]

for wave in waves:
    fig.add_vrect(
        x0=wave['start'],
        x1=wave['end'],
        fillcolor=wave['color'],
        opacity=0.5,
        layer="below",
        line_width=0)

fig.add_annotation(
    x=datetime(2020, 5, 6),
    y=df['Weekly cases per million people'].max() * 0.2,
    text="First wave<br>Spring 2020",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="black",
    ax=0,
    ay=-60,
    bgcolor="white",
    bordercolor="black",
    borderwidth=1,
    font=dict(size=16)
)

fig.add_annotation(
    x=datetime(2020, 12, 25),
    y=df['Weekly cases per million people'].max() * 0.4,
    text="Second wave<br>Winter-Spring 2020/2021",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="black",
    ax=0,
    ay=-60,
    bgcolor="white",
    bordercolor="black",
    borderwidth=1,
    font=dict(size=16)
)

fig.add_annotation(
    x=datetime(2021, 9, 5),
    y=df[df['Day'].dt.year == 2021]['Weekly cases per million people'].max() * 0.70,
    text="Delta variant<br>Summer 2021",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="black",
    ax=0,
    ay=-60,
    bgcolor="white",
    bordercolor="black",
    borderwidth=1,
    font=dict(size=16)
)

fig.add_annotation(
    x=datetime(2022, 1, 20),
    y=df['Weekly cases per million people'].max() * 1.05,
    text="Omicron variant<br>Winter 2022",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="black",
    ax=0,
    ay=-60,
    bgcolor="white",
    bordercolor="black",
    borderwidth=1,
    font=dict(size=16)
)

fig.update_layout(
    title=dict(
        text='Weekly confirmed COVID-19 cases per million people',
        font=dict(size=24, color='black', weight='bold'),
        x=0.55
    ),
    xaxis=dict(
        title='Date',
        title_font=dict(size=22, color='black', weight='bold'),
        title_standoff=20,
        linecolor='black',
        gridcolor='#E8E8E8',
        tickformat='%b-%Y',
        tickangle=-10,
        tickfont=dict(size=16, color='black'),
        dtick="M3",
        ticks='outside',
    ),
    yaxis=dict(
        title='Number of confirmed cases / 1M',
        title_font=dict(size=22, color='black', weight='bold'),
        title_standoff=30,
        linecolor='black',
        gridcolor='#E8E8E8',
        tickformat=',',
        tickfont=dict(size=16, color='black'),
        ticks='outside',
        range=[0, df['Weekly cases per million people'].max() * 1.25]
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    width=1400,
    height=700,
    margin=dict(l=150, r=50, t=100, b=100),
)

#fig.show()
#fig.write_html("../plots/confirmed_cases.html")
fig.write_html("../plots/confirmed_cases.html", include_plotlyjs='directory', full_html=True)