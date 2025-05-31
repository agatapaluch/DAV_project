import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as mticker
import matplotlib.dates as mdates


df = pd.read_csv("../data/cumulative-confirmed-covid-19-cases-per-million-people.csv")

df["Day"] = pd.to_datetime(df["Day"])
df = df.sort_values(by=["Day"])

countries = ["United States", "Poland", "Italy", "India", "United Kingdom", "Germany"]

df = df[df["Entity"].isin(countries)]

dates = pd.date_range(df["Day"].min(), df["Day"].max(), freq="ME")

colors = {
    "United States": "#E32763",
    "Italy": "#F57C36",
    "United Kingdom": "#4C9DF7",
    "Poland": "#F873F0",
    "India": "#3FEF67",
    "Germany": "#53ECF5"
}

fig, ax = plt.subplots(figsize=(12, 7))
plt.subplots_adjust(bottom=0.2)

def update(day):
    ax.clear()

    current_data = df[df["Day"] <= day]

    for country in countries:
        country_data = current_data[current_data["Entity"] == country]
        if not country_data.empty:
            last_point = country_data.iloc[-1]
            ax.scatter(last_point["Day"], last_point["Total confirmed cases of COVID-19 per million people"],
                       color=colors[country], label=country, s=30)
            ax.plot(country_data["Day"], country_data["Total confirmed cases of COVID-19 per million people"],
                    color=colors[country])
            ax.text(
                x=last_point["Day"] + pd.Timedelta(days=30),
                y=last_point["Total confirmed cases of COVID-19 per million people"],
                s=country,
                fontsize=11,
                fontweight='bold',
                color=colors[country],
                va='center'
            )

    ax.set_title("Cumulative confirmed COVID-19 cases per million people", fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel("Date", fontsize=16, fontweight='bold', labelpad=20)
    ax.set_ylabel("Total confirmed cases / 1M", fontsize=16, fontweight='bold', labelpad=20)

    ax.set_xlim(df["Day"].min(), df["Day"].max())
    max_cases = df["Total confirmed cases of COVID-19 per million people"].max()
    ax.set_ylim(0, max_cases * 1.05)

    ax.text(0.05, 0.89, day.strftime("%Y-%m-%d"), transform=ax.transAxes,
            fontsize=20, fontweight='bold', alpha=0.5)

    ax.grid(True, color="#E8E8E8", linestyle="--", linewidth=0.7)
    ax.tick_params(axis='both', labelsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x/1000)}k"))

    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    ax.tick_params(axis='x', rotation=15)

ani = animation.FuncAnimation(fig, update, frames=dates, interval=110, repeat=True)

#plt.show()
ani.save('../plots/cumulative_number_of_cases.gif', writer='Pillow', dpi=200)
