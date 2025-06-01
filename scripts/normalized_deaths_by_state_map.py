import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('../data/united_states_covid19_deaths_ed_visits_and_positivity_by_state.csv', skiprows=2)

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

df['state_code'] = df['State/Territory'].map(state_to_code)
df = df.dropna(subset=['state_code'])
df['Total Death rate per 100000'] = pd.to_numeric(df['Total Death rate per 100000'], errors='coerce')
df = df.dropna(subset=['Total Death rate per 100000'])

coords = pd.read_csv('../data/states_cords.csv')
coords = coords.rename(columns={'state': 'state_code'})
df = df.merge(coords[['state_code', 'latitude', 'longitude']], on='state_code', how='left')

max_val = df['Total Death rate per 100000'].max()

fig = px.choropleth(
    df,
    locations='state_code',
    color='Total Death rate per 100000',
    locationmode='USA-states',
    hover_name='State/Territory',
    color_continuous_scale='Blues',
    range_color=[0, max_val],
    labels={'Total Death rate per 100000': 'Total Deaths per 100k', 'state_code': 'State Code'},
    title='Death Rate per 100k Population by State (as of 17 May 2025)'
)

fig.add_trace(go.Scattergeo(
    locationmode='USA-states',
    lon=df.groupby('State/Territory')['longitude'].first(),
    lat=df.groupby('State/Territory')['latitude'].first(),
    text=df.groupby('State/Territory')['state_code'].first(),
    mode='text',
    textfont=dict(size=12, color='black', weight='bold'),
    hoverinfo='skip'
))


fig.update_layout(
    geo_scope='usa',
    geo=dict(lakecolor='white'),
    width=1200,
    height=800,
    title=dict(
        text='Death Rate per 100k Population by State (as of 17 May 2025)',
        x=0.5,
        font=dict(size=23, color='black', weight='bold'),
    ),
    coloraxis_colorbar=dict(
        title="Deaths per 100k",
        ticks="outside"
    )
)

#fig.show()
fig.write_html("../plots/normalized_deaths_by_state.html")
