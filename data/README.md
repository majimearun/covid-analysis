# Data

- Datasets in this repository get updated every 1 hour. (API used: [disease.sh](https://disease.sh/))
- Updating code: [update_data.py](https://github.com/majimearun/covid-analysis/blob/main/update_data.py)

## Datasets:

1. [country_confirmed.csv](country_confirmed.csv): timeseries for total number of confirmed cases in each country
2. [country_deaths.csv](country_deaths.csv): timeseries for total number of deaths in each country
3. [country_recovered.csv](country_recovered.csv): timeseries for total number of recovered cases in each country
4. [global_ts.csv](global_ts.csv): all 3 timeseries (confirmed, deaths, recovered) on global data
5. [vac_country.csv](vac_country.csv): timeseries for total number of vaccinated people in each country
6. [vac_global.csv](vac_global.csv): timeseries for total number of vaccinated people globally
7. [continents.csv](continents.csv): latest information on the pandemic split continent wise
8. [countries.csv](countries.csv): latest information on the pandemic split county wise

## Notes:

1. Most countries have stopped reporting number of recoveries daily, and shows only 0s for recent dates from the API currently used.
2. Except [global_ts.csv](global_ts.csv), [country_confirmed.csv](country_confirmed.csv),[country_deaths.csv](country_deaths.csv) and [country_recovered.csv](country_recovered.csv), the files are being used only for data analysis and visualization in the final dashbaord. The 4 mentioned csvs are being used for training our model and forecasting.
