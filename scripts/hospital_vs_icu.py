import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

def format_population(pop):
    if pop >= 1_000_000_000:
        return f"{pop / 1_000_000_000:.1f}B"
    elif pop >= 1_000_000:
        return f"{pop / 1_000_000:.1f}M"
    elif pop >= 1_000:
        return f"{pop / 1_000:.1f}K"
    else:
        return str(int(pop))

hospital_df = pd.read_csv("../data/current-covid-patients-hospital.csv")
icu_df = pd.read_csv("../data/current-covid-patients-icu.csv")

hospital_df = hospital_df[hospital_df["Entity"] == "United States"]
icu_df = icu_df[icu_df["Entity"] == "United States"]

hospital_df["Day"] = pd.to_datetime(hospital_df["Day"])
icu_df["Day"] = pd.to_datetime(icu_df["Day"])

hospital_df = hospital_df.sort_values("Day").set_index("Day")
icu_df = icu_df.sort_values("Day").set_index("Day")

start = max(hospital_df.index.min(), icu_df.index.min())
end = min(hospital_df.index.max(), icu_df.index.max())
date_range = pd.date_range(start, end)

hospital_df = hospital_df.reindex(date_range)
hospital_df["Daily hospital occupancy"] = hospital_df["Daily hospital occupancy"].astype(float).interpolate()

icu_df = icu_df.reindex(date_range)
icu_df["Daily ICU occupancy"] = icu_df["Daily ICU occupancy"].astype(float).interpolate()

dates = hospital_df.index
hospital_values = hospital_df["Daily hospital occupancy"]
icu_values = icu_df["Daily ICU occupancy"]

second_wave_start = pd.Timestamp("2020-10-01")
second_wave_end = pd.Timestamp("2021-03-31")
delta_start = pd.Timestamp("2021-05-01")
delta_end = pd.Timestamp("2021-10-31")
omicron_start = pd.Timestamp("2021-12-01")
omicron_end = pd.Timestamp("2022-03-31")

second_wave_peak = hospital_values[second_wave_start:second_wave_end].idxmax()
delta_peak = hospital_values[delta_start:delta_end].idxmax()
omicron_peak = hospital_values[omicron_start:omicron_end].idxmax()

monthly_dates = pd.date_range(start=start, end=end, freq="MS")
monthly_indices = [dates.get_loc(d) for d in monthly_dates if d in dates]
peak_dates = [second_wave_peak, delta_peak, omicron_peak]
peak_locs = [dates.get_loc(p) for p in peak_dates]

all_highlight_indices = sorted(set(monthly_indices + peak_locs))
highlight_indices = []
for idx in all_highlight_indices:
    highlight_indices.append(idx)
    if idx in peak_locs:
        highlight_indices.extend([idx] * 10)

fig, ax = plt.subplots(figsize=(10, 6))

line1, = ax.plot([], [], label="Hospital occupancy", color="blue")
line2, = ax.plot([], [], label="ICU occupancy", color="red")

date_text = ax.text(0.95, 0.85, "", transform=ax.transAxes,
                    ha="right", va="top", fontsize=15, fontweight="bold")

ax.legend(loc="upper right", frameon=True)

xticks = pd.date_range(start=start, end=end, freq="6MS")
ax.set_xticks(xticks)
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b %Y"))
ax.set_xlabel("Date", fontsize=15)

ymax = max(hospital_values.max(), icu_values.max()) * 1.3
yticks = plt.MaxNLocator(nbins=6).tick_values(0, ymax)
ax.set_yticks(yticks)
ax.set_yticklabels([format_population(y) for y in yticks])

ax.set_xlim(start, end)
ax.set_ylim(0, ymax)

ax.set_title("COVID-19: Hospital and ICU occupancy in the USA", fontweight="bold", fontsize=18, pad=15)
ax.set_ylabel("Occupancy", fontsize=15)
ax.grid(color="lightgrey")
plt.tight_layout()

second_wave_patch = ax.axvspan(second_wave_start, second_wave_end, color="orange", alpha=0.15)
delta_patch = ax.axvspan(delta_start, delta_end, color="red", alpha=0.15)
omicron_patch = ax.axvspan(omicron_start, omicron_end, color="blue", alpha=0.15)

second_wave_patch.set_visible(False)
delta_patch.set_visible(False)
omicron_patch.set_visible(False)

second_wave_annot = ax.annotate("Second wave\nWinter–Spring 2020/2021",
            xy=(second_wave_peak, hospital_values[second_wave_peak]),
            xytext=(second_wave_peak, hospital_values[second_wave_peak] + ymax * 0.1),
            ha="center",
            arrowprops=dict(facecolor="black", arrowstyle="->"),
            fontsize=10, bbox=dict(facecolor="white", edgecolor="gray"),
            visible=False)

delta_annot = ax.annotate("Delta variant\nSummer 2021",
            xy=(delta_peak, hospital_values[delta_peak]),
            xytext=(delta_peak, hospital_values[delta_peak] + ymax * 0.1),
            ha="center",
            arrowprops=dict(facecolor="black", arrowstyle="->"),
            fontsize=10, bbox=dict(facecolor="white", edgecolor="gray"),
            visible=False)

omicron_annot = ax.annotate("Omicron variant\nWinter 2022",
            xy=(omicron_peak, hospital_values[omicron_peak]),
            xytext=(omicron_peak, hospital_values[omicron_peak] + ymax * 0.1),
            ha="center",
            arrowprops=dict(facecolor="black", arrowstyle="->"),
            fontsize=10, bbox=dict(facecolor="white", edgecolor="gray"),
            visible=False)

def plot(i):
    idx = highlight_indices[i]
    current_date = dates[idx]

    line1.set_data(dates[:idx], hospital_values[:idx])
    line2.set_data(dates[:idx], icu_values[:idx])
    date_text.set_text(current_date.strftime("%b %Y"))

    if current_date >= second_wave_start:
        second_wave_patch.set_visible(True)
    if current_date >= delta_start:
        delta_patch.set_visible(True)
    if current_date >= omicron_start:
        omicron_patch.set_visible(True)

    if current_date >= second_wave_peak:
        second_wave_annot.set_visible(True)
    if current_date >= delta_peak:
        delta_annot.set_visible(True)
    if current_date >= omicron_peak:
        omicron_annot.set_visible(True)

    return line1, line2, date_text, second_wave_patch, delta_patch, omicron_patch, second_wave_annot, delta_annot, omicron_annot

ani = animation.FuncAnimation(fig, plot, frames=len(highlight_indices), interval=500, repeat=True)
ani.save("../plots/usa_hospital_icu.gif", writer="pillow", dpi=300)
