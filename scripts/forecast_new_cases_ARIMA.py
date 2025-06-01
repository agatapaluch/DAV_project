import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

def format_population(pop):
    if pop >= 1_000_000_000:
        return f"{pop / 1_000_000_000:.1f}B"
    elif pop >= 1_000_000:
        return f"{pop / 1_000_000:.1f}M"
    elif pop >= 1_000:
        return f"{pop / 1_000:.1f}K"
    else:
        return str(int(pop))

df = pd.read_csv("../data/weekly-confirmed-covid-19-cases-per-million-people.csv")
df["Day"] = pd.to_datetime(df["Day"])
us_data = df[df["Entity"] == "United States"].copy()
us_data.set_index("Day", inplace=True)

weekly_series = us_data["Weekly cases per million people"].resample("W").mean()

forecast_horizon = 52
train_series = weekly_series.iloc[:-forecast_horizon]
test_series = weekly_series.iloc[-forecast_horizon:]

model = ARIMA(train_series, order=(5, 1, 5)).fit()
forecast_result = model.get_forecast(steps=forecast_horizon)
forecast = forecast_result.predicted_mean
conf_int = forecast_result.conf_int(alpha=0.05)

plt.figure(figsize=(14, 8))
plt.plot(weekly_series.index, weekly_series.values, "k-", label="Original data")
plt.plot(forecast.index, forecast.values, "b-", linewidth=2, label="Forecast")
plt.fill_between(forecast.index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color="blue", alpha=0.15, label="95% CI")
plt.plot(test_series.index, test_series.values, label="Actual data", color="red")
plt.axvline(train_series.index[-1], color="gray", linestyle="--")

plt.annotate("Forecast start",
             xy=(train_series.index[-1], train_series.iloc[-1]),
             xytext=(10, 170),  
             textcoords="offset points",
             ha="left",
             fontsize=10,
             color="black",
             fontweight="bold")

plt.title("COVID-19: Weekly new cases forecast with ARIMA", fontsize=20, weight="bold", pad=15)
plt.xlabel("Date", fontsize=16)
plt.ylabel("Number of confirmed cases / 1M", fontsize=16)
plt.grid(color="#ebebea")
plt.legend(loc="upper left")

plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: format_population(y)))

plt.tight_layout()
plt.savefig("../plots/usa_covid_weekly_forecast_ARIMA.png", dpi=300)


