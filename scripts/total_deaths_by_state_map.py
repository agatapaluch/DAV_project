import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('../data/us-states.csv')
df['date'] = pd.to_datetime(df['date'])

state_to_code = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
    'District of Columbia': 'DC'
}

df['state_code'] = df['state'].map(state_to_code)
df = df.dropna(subset=['state_code'])

coords = pd.read_csv('../data/states_cords.csv')
coords = coords.rename(columns={'state': 'state_code'})
df = df.merge(coords[['state_code', 'latitude', 'longitude']], on='state_code', how='left')

df_monthly = df[df['date'].dt.day == 1]
df_monthly = df_monthly.copy()
df_monthly['date_str'] = df_monthly['date'].dt.strftime('%Y-%m-%d')

unique_dates = df_monthly['date'].sort_values().unique()
steps = []
for d in unique_dates:
    steps.append(dict(
        method="animate",
        label=pd.to_datetime(d).strftime("%b %Y"),
        args=[["{}".format(pd.to_datetime(d).strftime('%Y-%m-%d'))],
              {"frame": {"duration": 300, "redraw": True},
               "mode": "immediate",
               "transition": {"duration": 200}}],
    ))

fig = px.choropleth(
    df_monthly,
    locations='state_code',
    color='deaths',
    locationmode='USA-states',
    animation_frame='date_str',
    hover_name='state',
    hover_data={'deaths': ':,.0f', 'cases': ':,.0f','date_str': True,'date': False, 'state_code': True},
    color_continuous_scale='Blues',
    labels={'deaths': 'Total Deaths', 'cases': 'Total Cases', 'date_str': 'Date', 'state_code': 'State Code'},
    range_color=[0, df_monthly['deaths'].max()],
    title='Total Number of COVID-19 Deaths by State over time',
)

fig.add_trace(go.Scattergeo(
    locationmode='USA-states',
    lon=df_monthly.groupby('state')['longitude'].first(),
    lat=df_monthly.groupby('state')['latitude'].first(),
    text=df_monthly.groupby('state')['state_code'].first(),
    mode='text',
    textfont=dict(size=12, color='black', weight='bold'),
    hoverinfo='skip'
))

fig.update_layout(
    geo_scope='usa',
    geo=dict(lakecolor='white'),
    title=dict(
        text='Total Number of COVID-19 Deaths by State over time',
        x=0.5,
        font=dict(size=23, color='black', weight='bold'),
    ),
    width=1200,
    height=800,
    sliders=[dict(
        active=0,
        steps=steps,
        currentvalue=dict(prefix="Date: ", font=dict(size=20)),
        x=0.1, len=0.85
    )],
    updatemenus=[dict(
        type="buttons",
        x=-0.05, xanchor="left", y=0, yanchor="top",
        buttons=[
            dict(label="Play", method="animate",
                 args=[None, {
                     "frame": {"duration": 300, "redraw": True},
                     "fromcurrent": True,
                     "transition": {"duration": 100}
                 }]),
            dict(label="Pause", method="animate",
                 args=[[None], {
                     "frame": {"duration": 0, "redraw": True},
                     "mode": "immediate",
                     "transition": {"duration": 0}
                 }])
        ]
    )]
)

#fig.show()
fig.write_html("../plots/total_deaths_by_state_map.html")
