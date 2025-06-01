import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df_unemployment = pd.read_csv('../data/bls_unemployment_rate_per_state.csv')

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

df_long = pd.melt(df_unemployment,
                  id_vars=['State'],
                  var_name='date_str',
                  value_name='unemployment_rate')

month_year_to_date = {}
for col in df_unemployment.columns[1:]:
    try:
        month, year = col.split(' ')
        month_num = {
            'January': '01', 'February': '02', 'March': '03', 'April': '04',
            'May': '05', 'June': '06', 'July': '07', 'August': '08',
            'September': '09', 'October': '10', 'November': '11', 'December': '12'
        }[month]
        date_str = f"{year}-{month_num}-01"
        month_year_to_date[col] = date_str
    except:
        continue

df_long['date'] = df_long['date_str'].map(month_year_to_date)
df_long = df_long.dropna(subset=['date'])
df_long['date'] = pd.to_datetime(df_long['date'])

df_long['state_code'] = df_long['State'].map(state_to_code)
df_long = df_long.dropna(subset=['state_code'])

df_long['unemployment_rate'] = pd.to_numeric(df_long['unemployment_rate'], errors='coerce')
df_long = df_long.dropna(subset=['unemployment_rate'])

df_long['date_str_formatted'] = df_long['date'].dt.strftime('%Y-%m-%d')

unique_dates = df_long['date'].sort_values().unique()
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
    df_long,
    locations='state_code',
    color='unemployment_rate',
    locationmode='USA-states',
    animation_frame='date_str_formatted',
    hover_name='State',
    hover_data={'unemployment_rate': ':.1f%', 'date_str_formatted': True, 'state_code': True},
    color_continuous_scale='oranges',
    labels={'unemployment_rate': 'Unemployment rate (%)', 'date_str_formatted': 'Date', 'state_code': 'State Code'},
    range_color=[0, df_long['unemployment_rate'].max()],
    title='Unemployment Rate by State over time',
)

coords = pd.read_csv('../data/states_cords.csv')
coords = coords.rename(columns={'state': 'state_code'})
df_with_coords = df_long.merge(coords[['state_code', 'latitude', 'longitude']], on='state_code', how='left')

fig.add_trace(go.Scattergeo(
    locationmode='USA-states',
    lon=df_with_coords.groupby('State')['longitude'].first(),
    lat=df_with_coords.groupby('State')['latitude'].first(),
    text=df_with_coords.groupby('State')['state_code'].first(),
    mode='text',
    textfont=dict(size=10, color='black', weight='bold'),
    hoverinfo='skip'
))

fig.update_layout(
    geo_scope='usa',
    geo=dict(lakecolor='white'),
    title=dict(
        text='Unemployment Rate by State over time',
        x=0.5,
        font=dict(size=23, color='black', weight='bold'),
    ),
    width=1200,
    height=800,
    sliders=[dict(
        active=0,
        steps=steps,
        currentvalue=dict(prefix="Date: ", font=dict(size=16)),
        x=0.1, len=0.85
    )],
    updatemenus=[dict(
        type="buttons",
        x=-0.05, xanchor="left", y=0, yanchor="top",
        buttons=[
            dict(label="Play", method="animate",
                 args=[None, {
                     "frame": {"duration": 400, "redraw": True},
                     "fromcurrent": True,
                     "transition": {"duration": 200}
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

fig.update_coloraxes(
    colorbar_title_text="Unemployment rate [%]",
    colorbar_title_font_size=14
)

#fig.show()
fig.write_html("../plots/unemployment_per_state.html")
