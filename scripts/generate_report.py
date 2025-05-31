from pathlib import Path

PLOTS_DIR = Path("../plots")
OUTPUT_FILE = "../reports/usa_report.html"

custom_order = [
    'confirmed_cases.html', 'confirmed_deaths.html', 'cumulative_number_of_cases.gif',
    'cumulative_number_of_deaths.gif', 'total_deaths_by_state_map.html',
    'normalized_deaths_by_state.html', 'usa_vaccinations.png', 'state_vaccination_trends.html',
    'usa_hospital_vs_new_cases.gif', 'usa_hospital_icu.gif', 'usa_covid_weekly_forecast_ARIMA.png',
    'usa_covid_weekly_forecast_SARIMA.png', 'covid_cases_colleges_map.html', 'stay_home_orders_usa.html',
    'economic_indicators.html', 'unemployment_per_state.html'
]

custom_titles = {
    'normalized_deaths_by_state.html': 'Normalized Deaths By State Map',
    'usa_vaccinations.png': 'Countrywide Vaccination Trends',
    'usa_hospital_vs_new_cases.gif': 'Hospital admissions vs new cases',
    'usa_hospital_icu.gif': 'Hospital vs ICU occupancy',
    'usa_covid_weekly_forecast_ARIMA.png': 'Weekly new cases forecast with ARIMA',
    'usa_covid_weekly_forecast_SARIMA.png': 'Weekly new cases forecast with SARIMA',
    'stay_home_orders_usa.html': 'Statewide stay-at-home orders',
    'unemployment_per_state.html': 'Unemployment rate per state'}

plot_descriptions = {
    'confirmed_cases.html': 'Interactive visualization showing the progression of confirmed COVID-19 cases across different time periods.',
    'confirmed_deaths.html': 'Interactive visualization showing the progression of confirmed COVID-19 deaths across different time periods.',
    'cumulative_number_of_cases.gif': 'Animated plot showing the cumulative number of confirmed COVID-19 cases in comparison to other countries',
    'cumulative_number_of_deaths.gif': 'Animated plot showing the cumulative number of confirmed COVID-19 deaths in comparison to other countries',
    'total_deaths_by_state_map.html': 'Map displaying total number of COVID-19 deaths by state with interactive features.',
    'normalized_deaths_by_state.html': 'Map displaying death rate per 100 000 people by state with interactive features.',
    'usa_vaccinations.png': 'Overview of COVID-19 vaccination trends (full, 1 dose, boosters) countrywide.',
    'state_vaccination_trends.html': 'Interactive overview of COVID-19 vaccination trends (full, 1 dose, boosters) statewide.',
    'usa_hospital_vs_new_cases.gif': 'Animated plot showing weekly COVID-19 hospital admissions compared to weekly new cases.',
    'usa_hospital_icu.gif': 'Animated plot showing COVID-19 related hospital vs ICU occupancy.',
    'usa_covid_weekly_forecast_ARIMA.png': 'Statistical forecasting model (ARIMA) predicting weekly new cases vs actual data.',
    'usa_covid_weekly_forecast_SARIMA.png': 'Statistical forecasting model (SARIMA) predicting weekly new cases vs actual data.',
    'covid_cases_colleges_map.html': 'Cumulative COVID-19 cases in US colleges during the 2020/2021 academic year',
    'stay_home_orders_usa.html': 'Map visualizing states that did (or did not) issue a stay-at-home order in response to the pandemic',
    'economic_indicators.html': 'Interactive plot showing how economic indicators such as unemployment rate, export and import were affected during COVID-19 outbreak.',
    'unemployment_per_state.html': 'Map displaying state-level unemployment rate changes throughout the years.'
}

custom_sizes = {
    'confirmed_cases.html': (1400, 700),
    'confirmed_deaths.html': (1400, 700),
}

def collect_files(directory):
    return {
        f.name: f
        for f in directory.rglob("*")
        if f.suffix in [".png", ".gif", ".html"]
    }

def generate_html(ordered_files):
    html_parts = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "<meta charset='UTF-8'>",
        "<title>COVID-19 Analysis Report - United States</title>",
        "<style>",
        "  body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; background: #fafafa; }",
        "  .container { max-width: 1600px; margin-left: 30px; padding: 20px; }",
        "  h1 { color: #d32f2f; border-bottom: 3px solid #081747; padding-bottom: 10px; }",
        "  h2 { color: #081747; margin-top: 40px; margin-bottom: 5px; }",
        "  .summary { background: #081747; padding: 20px; border-left: 4px solid #d32f2f; margin: 20px 0; color: #FFFFFF; }",
        "  .key-stats { display: flex; justify-content: space-around; margin: 30px 0; }",
        "  .stat-box { text-align: center; padding: 15px; background: #081747; border-radius: 8px; color: #d32f2f }",
        "  .stat-number { font-size: 2em; font-weight: bold; color: #FFFFFF; }",
        "  .shift-left { transform: translateX(-35px); }",
        "  .centered { display: block; margin-left: auto; margin-right: auto; }",
        "  img, iframe { display: block; margin-bottom: 20px; border: 1px solid #ccc; }",
        "  .plot-title { text-align: center; margin-bottom: 10px; }",
        "  .plot-description { text-align: center; font-style: italic; color: #666; margin-bottom: 15px; }",
        "</style>",
        "</head>",
        "<body>",
        "<div class='container'>",
        "<h1>COVID-19 Analysis Report: United States</h1>",
        "",
        "<div class='summary'>",
        "<p><strong>Executive Summary:</strong> Project for Data analysis and visualization that shows statistics, "
        "trends and predictions for COVID-19 pandemic in the United States of America.<br>This project presents a comprehensive data analysis and visualization"
        " of COVID-19 infection, death rates, vaccination trends, hospitalization occupancy lockdown orders and "
        "economic indicators at both national and state levels. It also highlights the difference between forecasted "
        "infection rates and actual COVID-19 data.</p>",
        "</div>",
        "",
        "<div class='key-stats'>",
        "<div class='stat-box'>",
        "<div class='stat-number'>103M+</div>",
        "<div>Total Cases</div>",
        "</div>",
        "<div class='stat-box'>",
        "<div class='stat-number'>1.2M+</div>",
        "<div>Total Deaths</div>",
        "</div>",
        "<div class='stat-box'>",
        "<div class='stat-number'>347M</div>",
        "<div>Population</div>",
        "</div>",
        "<div class='stat-box'>",
        "<div class='stat-number'>206M+</div>",
        "<div>Vaccinations</div>",
        "</div>",
        "</div>",
        "",
        "<h2>Data source:</h2>",
        "<p>Data was collected from multiple sources including Centers for Disease Control and Prevention or US Bureau Of Labor Statistics.</p>"
        "",
        "<h2>Included plots:</h2>",
        "<ul>",
        "<li>New weekly confirmed COVID-19 cases and deaths countrywide.</li>",
        "<li>Cumulative COVID-19 cases and deaths comparing the USA to other countries.</li>"
        "<li>Total number of COVID-19-related deaths statewide.</li>",
        "<li>COVID-19 vaccination trends (full, 1 dose, boosters) both country and statewide.</li>",
        "<li>Weekly COVID-19 hospital admissions compared to weekly new cases.</li>",
        "<li>COVID-19 related hospital vs ICU occupancy.</li>",
        "<li>Forecasts of new cases vs actual data.</li>",
        "<li>Cumulative COVID-19 cases in US colleges during the 2020/2021 academic year.</li>",
        "<li>Statewide stay-at-home orders.</li>",
        "<li>Economic indicators - unemployment rate, import/export prices.</li>",
        "</ul>",
        ""
    ]

    for name, path in ordered_files:
        # if title not specified, use specific format
        if name in custom_titles:
            display_name = custom_titles[name]
        else:
            display_name = name.replace('_', ' ').replace('-', ' ').title().replace('.Html', '').replace('.Png', '').replace('.Gif', '')

        html_parts.append(f"<div class='plot-title'><h2>{display_name}</h2></div>")

        # add description if specified
        if name in plot_descriptions:
            html_parts.append(f"<div class='plot-description'>{plot_descriptions[name]}</div>")

        width, height = custom_sizes.get(name, (1200, 800))

        if name in ["confirmed_cases.html", "confirmed_deaths.html"]:
            extra_class = "shift-left"
        else:
            extra_class = "centered"

        if path.suffix in [".png", ".gif"]:
            import base64
            with open(path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
                mime_type = "image/png" if path.suffix == ".png" else "image/gif"
                html_parts.append(
                    f"<img src='data:{mime_type};base64,{img_data}' width='{width}' height='{height}' class='{extra_class}'>"
                )
        elif path.suffix == ".html":
            with open(path, encoding="utf-8") as html_file:
                embedded_html = html_file.read()
            html_parts.append(f"""
                <div class="{extra_class}" style="margin: 0 auto 30px; text-align: center;">
                    <div style="display: inline-block; max-width: 100%; text-align: center;">
                        {embedded_html}
                    </div>
                </div>
            """)

    html_parts.extend([
        "",
        "<div class='summary' style='margin-top: 40px;'>",
        f"<p><strong>Report Generated:</strong> {__import__('datetime').datetime.now().strftime('%B %d, %Y at %H:%M UTC')}<br>",
        "<strong>Authors:</strong> Barbara Pawlowska, Agata Paluch</p>",
        "</div>",
        "",
        "</div></body></html>"
    ])

    return "\n".join(html_parts)


def main():
    all_files = collect_files(PLOTS_DIR)

    ordered = [(name, all_files[name]) for name in custom_order if name in all_files]

    remaining = sorted(
        (name, path) for name, path in all_files.items()
        if name not in custom_order
    )
    ordered.extend(remaining)

    html = generate_html(ordered)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report saved as: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()