import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import colorsys

df = pd.read_csv("../data/us_state_vaccinations.csv")
df["date"] = pd.to_datetime(df["date"])

us_states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
    "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana",
    "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
    "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
    "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina",
    "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
    "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]
df = df[df["location"].isin(us_states)]

metrics = [
    "people_fully_vaccinated_per_hundred",
    "people_vaccinated_per_hundred",
    "total_boosters_per_hundred"
]
metric_labels = {
    "people_fully_vaccinated_per_hundred": "People fully vaccinated",
    "people_vaccinated_per_hundred": "People vaccinated with at least 1 dose",
    "total_boosters_per_hundred": "Total bootsters given"
}

states = sorted(df["location"].unique())

def generate_50_distinct_colors():
    colors = []
    for i in range(50):
        hue = i / 50
        saturation = 0.6  
        value = 0.8       
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        color_str = f"rgba({int(r*255)}, {int(g*255)}, {int(b*255)}, 1)"
        colors.append(color_str)
    return colors

colors = generate_50_distinct_colors()

fig = go.Figure()

for metric_index, metric in enumerate(metrics):
    for state_idx, state in enumerate(states):
        state_df = df[df["location"] == state]
        visible = (metric_index == 0)
        fig.add_trace(go.Scatter(
            x=state_df["date"],
            y=state_df[metric],
            mode="lines+markers",
            name=state,
            legendgroup=state,
            showlegend=True if metric_index == 0 else False,
            visible=visible,
            line=dict(color=colors[state_idx], width=1),
            marker=dict(color=colors[state_idx], size=2)
        ))

buttons = []
num_states = len(states)
for i, metric in enumerate(metrics):
    visibility = [False] * (num_states * len(metrics))
    for j in range(num_states):
        visibility[i * num_states + j] = True
    buttons.append(dict(
        label=metric_labels[metric],
        method="update",
        args=[{"visible": visibility, "showlegend": True}, {}]
    ))

fig.update_layout(
    title=dict(
        text="COVID-19 vaccination trends in USA by state",
        font=dict(color="black", size=30, family="Arial", weight="bold"),
        x=0.4,
    ),
    width=1300,
    height=800,
    xaxis_title=dict(
        text="Date",
        font=dict(color="black", size=20)
    ),
    yaxis_title=dict(
        text="Vaccination per 100 people",
        font=dict(color="black", size=20)
    ),
    xaxis=dict(
        range=[df["date"].min(), df["date"].max()],
        showgrid=True,
        gridcolor="lightgrey",
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="lightgrey",
    ),
    plot_bgcolor="white",
    updatemenus=[
        dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            x=1.02,
            y=1.10,
            xanchor="left",
            yanchor="top"
        )
    ],
    legend=dict(
        title=dict(
            text="                 State",  
            font=dict(size=14, color="black", weight="bold"),
            side="top"
        ),
        orientation="v",
        x=1.05,
        y=1,
        xanchor="left",
        bgcolor="white",
        bordercolor="black",
        borderwidth=1,
        font=dict(color="black", size=12),
        traceorder="normal",
        valign="middle",
        itemsizing="constant",
        itemwidth=90,
        itemclick="toggle",
        itemdoubleclick="toggleothers",
    ),
)

fig.write_html("../plots/state_vaccination_trends.html")
