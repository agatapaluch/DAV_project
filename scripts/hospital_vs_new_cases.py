import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

pop_usa = 347_099_192

admissions_df = pd.read_csv("../data/weekly-hospital-admissions-covid.csv")
admissions_df = admissions_df[admissions_df['Entity'] == 'United States']
admissions_df['Day'] = pd.to_datetime(admissions_df['Day'])
admissions_df = admissions_df.sort_values('Day').set_index('Day')
admissions_df = admissions_df[['Weekly new hospital admissions']].astype(float)

cases_df = pd.read_csv("../data/weekly-confirmed-covid-19-cases-per-million-people.csv")
cases_df = cases_df[cases_df['Entity'] == 'United States']
cases_df['Day'] = pd.to_datetime(cases_df['Day'])
cases_df = cases_df.sort_values('Day').set_index('Day')
cases_df = cases_df[['Weekly cases per million people']].astype(float)

start = max(admissions_df.index.min(), cases_df.index.min())
end = min(admissions_df.index.max(), cases_df.index.max())
date_range = pd.date_range(start, end)

admissions_df = admissions_df.reindex(date_range).interpolate()
cases_df = cases_df.reindex(date_range).interpolate()

dates = admissions_df.index
admissions_per_million = admissions_df['Weekly new hospital admissions'] / (pop_usa / 1_000_000)
cases_values = cases_df['Weekly cases per million people']

delta_start = pd.Timestamp("2021-05-01")
delta_end = pd.Timestamp("2021-10-31")
omicron_start = pd.Timestamp("2021-12-01")
omicron_end = pd.Timestamp("2022-03-31")

delta_peak = cases_values[delta_start:delta_end].idxmax()
omicron_peak = cases_values[omicron_start:omicron_end].idxmax()

monthly_dates = pd.date_range(start=start, end=end, freq='MS')
monthly_indices = [dates.get_loc(d) for d in monthly_dates if d in dates]
peak_dates = [delta_peak, omicron_peak]
peak_locs = [dates.get_loc(p) for p in peak_dates]

highlight_indices = []
for idx in sorted(set(monthly_indices + peak_locs)):
    highlight_indices.append(idx)
    if idx in peak_locs:
        highlight_indices.extend([idx] * 10)

fig, ax = plt.subplots(figsize=(10, 6))
line1, = ax.plot([], [], label='Weekly hospital admissions', color='blue')
line2, = ax.plot([], [], label='Weekly new cases ', color='red')
date_text = ax.text(0.02, 0.90, '', transform=ax.transAxes,
                    ha='left', va='top', fontsize=15, fontweight='bold')

ax.legend(loc='upper right', frameon=True)
xticks = pd.date_range(start=start, end=end, freq='6MS')
ax.set_xticks(xticks)
ax.set_xticklabels([d.strftime('%b %Y') for d in xticks])
ax.set_xlabel("Date", fontsize=15)

ymax = max(admissions_per_million.max(), cases_values.max()) * 1.3
ax.set_ylim(0, ymax)
ax.set_xlim(start, end)
ax.set_ylabel("Number of people / 1M", fontsize=15)
ax.set_title("COVID-19: Weekly hospital admissions and new cases per million",
             fontweight='bold', fontsize=16, pad=15)
ax.grid(color = "lightgrey")
plt.tight_layout()

delta_patch = ax.axvspan(delta_start, delta_end, color='blue', alpha=0.15, visible=False)
omicron_patch = ax.axvspan(omicron_start, omicron_end, color='red', alpha=0.15, visible=False)

delta_annot = ax.annotate("Delta variant\nSummer 2021",
                         xy=(delta_peak, cases_values[delta_peak]),
                         xytext=(delta_peak, cases_values[delta_peak] + ymax * 0.1),
                         ha='center',
                         arrowprops=dict(facecolor='black', arrowstyle="->"),
                         fontsize=10, bbox=dict(facecolor='white', edgecolor='gray'),
                         visible=False)

omicron_annot = ax.annotate("Omicron variant\nWinter 2022",
                           xy=(omicron_peak, cases_values[omicron_peak]),
                           xytext=(omicron_peak, cases_values[omicron_peak] + ymax * 0.1),
                           ha='center',
                           arrowprops=dict(facecolor='black', arrowstyle="->"),
                           fontsize=10, bbox=dict(facecolor='white', edgecolor='gray'),
                           visible=False)

def plot(i):
    idx = highlight_indices[i]
    current_date = dates[idx]
    line1.set_data(dates[:idx], admissions_per_million[:idx])
    line2.set_data(dates[:idx], cases_values[:idx])
    date_text.set_text(current_date.strftime('%b %Y'))
    if current_date >= delta_start:
        delta_patch.set_visible(True)
    if current_date >= omicron_start:
        omicron_patch.set_visible(True)
    if current_date >= delta_peak:
        delta_annot.set_visible(True)
    if current_date >= omicron_peak:
        omicron_annot.set_visible(True)
    return line1, line2, date_text, delta_patch, omicron_patch, delta_annot, omicron_annot

ani = animation.FuncAnimation(fig, plot, frames=len(highlight_indices), interval=300, repeat=True)
ani.save("../plots/usa_hospital_vs_new_cases.gif", writer='pillow', dpi=300)
