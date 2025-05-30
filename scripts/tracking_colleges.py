import pandas as pd
import plotly.express as px

df_cases = pd.read_csv("../data/colleges.csv")      
df_colleges = pd.read_csv("../data/colleges_cords.csv")

df_cases["ipeds_id"] = df_cases["ipeds_id"].astype(str)
df_colleges["UNITID"] = df_colleges["UNITID"].astype(str)

coords_dict = df_colleges.set_index("UNITID")[["LATITUDE", "LONGITUDE", "STATE", "INSTNM", "STABBR"]].to_dict("index")

def get_college_info(ipeds):
    info = coords_dict.get(ipeds, {})
    return pd.Series({
        "LATITUDE": info.get("LATITUDE"),
        "LONGITUDE": info.get("LONGITUDE"),
        "STATE": info.get("STATE"),
        "STABBR": info.get("STABBR"),
        "INSTNM": info.get("INSTNM")
    })

df_cases = df_cases.join(df_cases["ipeds_id"].apply(get_college_info))
df_cases = df_cases.dropna(subset=["LATITUDE", "LONGITUDE"])

fig = px.scatter_geo(
    df_cases,
    lat="LATITUDE",
    lon="LONGITUDE",
    size="cases",
    color="cases",
    labels={"cases": "Cases"},
    color_continuous_scale=[
        [0.0, "#FFFFFF"],
        [0.25, "#a7cce2"],
        [0.5, "#458ebe"],
        [0.75, "#20405D"],
        [1.0, "#010203"]
    ],
    hover_name="INSTNM",
    hover_data={
        "STATE": True,
        "cases": True,
        "LATITUDE": False,
        "LONGITUDE": False
    },
    size_max=25,
    projection="albers usa",
    title="COVID-19: Cases in academic year 2020/2021 in colleges in USA"
)

fig.update_traces(marker=dict(line=dict(width=1, color="#8A96A1")))

fig.update_layout(
    title=dict(
        text="COVID-19: Cases in the academic year 2020/2021 in colleges in USA",
        x=0.5,
        font=dict(color="black", size=20, family="Arial", weight="bold")
    )
)

state_labels = df_cases.groupby("STABBR").agg({"LATITUDE": "mean", "LONGITUDE": "mean"}).reset_index()
state_labels.loc[state_labels["STABBR"] == "NY", "LATITUDE"] += 1.5

fig.add_scattergeo(
    locations=None,
    lon=state_labels["LONGITUDE"],
    lat=state_labels["LATITUDE"],
    text=state_labels["STABBR"],
    mode="text",
    showlegend=False,
    textfont=dict(color="#20405D", size=12, weight="bold")
)

fig.write_html("../plots/covid_cases_colleges_map.html")
