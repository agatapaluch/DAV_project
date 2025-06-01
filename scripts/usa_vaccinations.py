import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv("../data/us_state_vaccinations.csv")

us_states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

df = df[df["location"].isin(us_states)]

df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

monthly_avg = df.groupby("month")[[
    "people_vaccinated_per_hundred",
    "people_fully_vaccinated_per_hundred",
    "total_boosters_per_hundred"
]].mean(numeric_only=True).reset_index()

plt.figure(figsize=(14, 8))
plt.plot(monthly_avg["month"], monthly_avg["people_vaccinated_per_hundred"], label="At least 1 dose", color="darkblue")
plt.plot(monthly_avg["month"], monthly_avg["people_fully_vaccinated_per_hundred"], label="Fully vaccinated", color="lightblue")
plt.plot(monthly_avg["month"], monthly_avg["total_boosters_per_hundred"], label="Total boosters", color="darkgreen")

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.xlabel("Date", fontsize=16, fontweight='bold')
plt.ylabel("Vaccination per 100 people", fontsize=16, fontweight='bold')
plt.title("COVID-19 vaccination trends in the USA ", fontweight="bold", fontsize=18, pad=15)
plt.legend()
plt.grid(color="lightgrey")
plt.tight_layout()

plt.savefig("../plots/usa_vaccinations.png", dpi=300)
