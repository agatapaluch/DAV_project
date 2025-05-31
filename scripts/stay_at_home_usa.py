import pandas as pd
import plotly.express as px

no_order_states = ["Arkansas", "Iowa", "Nebraska", "North Dakota", "South Dakota", "Utah", "Wyoming"]

df_states = pd.read_csv("../data/states_cords.csv")

df_states["stay_home_status_label"] = df_states["name"].apply(
    lambda x: "No statewide order" if x in no_order_states else "Issued stay-at-home order"
)

fig = px.choropleth(
    df_states,
    locations="state",
    locationmode="USA-states",
    color="stay_home_status_label",
    color_discrete_map={
        "Issued stay-at-home order": "#6ea9d1",
        "No statewide order": "#a7cce2"
    },
    scope="usa",
    hover_name="name",
    hover_data={
        "stay_home_status_label": True,
        "state": False,
        "latitude": False,
        "longitude": False
    },
    labels={
        "stay_home_status_label": "Order Status"
    },
)

fig.add_scattergeo(
    lon=df_states["longitude"],
    lat=df_states["latitude"],
    text=df_states["state"],
    mode="text",
    textfont=dict(color="black", size=12, family="Arial", weight="bold"),
    showlegend=False,
    hoverinfo="skip"
)

fig.update_layout(
    title=dict(
        text="COVID-19: Statewide stay-at-home order in the USA (March–April 2020)",
        x=0.5,
        font=dict(color="black", size=26, family="Arial", weight="bold")
    ),
    margin=dict(l=0, r=0, t=50, b=0),
    legend_title_text="Stay-at-home order",
    legend_title_font=dict(
        size=16,
        color="black",
        family="Arial",
        weight="bold"
    ),
    legend=dict(
        font=dict(size=14, color="black", family="Arial"),
        itemsizing="constant"
    ),
    geo=dict(
        lakecolor="rgb(255, 255, 255)",
        bgcolor="rgba(0,0,0,0)"
    )
)

fig.update_traces(marker_line_color="#20405D", marker_line_width=1)

fig.write_html("../plots/stay_home_orders_usa.html")
