# Imports
import pandas as pd
import requests
import pickle

base_url = "https://disease.sh/v3/covid-19"


def get_global_update(url=base_url, save=False):

    """
    Args:
        url (str, optional): common/home part of url used to derive other urls from which we get required information. Defaults to base_url
        save (bool, optional): arg determing whether the content gathered/updated should be saved or not. Defaults to False
    Returns:
        dict: dictionary with information of cases updated most recently today
    """

    global_url = url + "/all"

    global_update = requests.get(global_url).json()

    if save:
        with open("./data/global_update.pkl", "wb") as file:
            pickle.dump(global_update, file)

    return global_update


def get_continent_update(url=base_url, save=False):
    """
    Args:
        url (string, optional): common/home part of url used to derive other urls from which we get required information. Defaults to base_url
        save (bool, optional): arg determing whether the content gathered/updated should be saved or not. Defaults to False
    Returns:
        pd.DataFrame: a dataframe with the most recent updated cases segregated continent wise
    """
    continents_url = url + "/continents"

    continents_updates = requests.get(continents_url).json()

    continents = [
        {
            "continent": i["continent"],
            "lat": i["continentInfo"]["lat"],
            "long": i["continentInfo"]["long"],
            "confirmed_cumulative": i["cases"],
            "confirmed_new": i["todayCases"],
            "deaths_cumulative": i["deaths"],
            "deaths_new": i["todayDeaths"],
            "recovered_cumulative": i["recovered"],
            "recovered_new": i["todayRecovered"],
            "active": i["active"],
            "critical": i["critical"],
            "updated": i["updated"],
        }
        for i in continents_updates
    ]

    continents_df = pd.DataFrame(continents, columns=continents[0].keys())

    if save:
        continents_df.to_csv("./data/continents.csv", index=False)

    return continents_df


def get_country_update(url=base_url, save=False):
    """
    Args:
        url (string, optional): common/home part of url used to derive other urls from which we get required information. Defaults to base_url
        save (bool, optional): arg determing whether the content gathered/updated should be saved or not. Defaults to False
    Returns:
        pd.DataFrame: a dataframe with the most recent updated cases segregated country wise
    """

    countries_url = url + "/countries"

    countries_updates = requests.get(countries_url).json()

    countries = [
        {
            "country": i["country"],
            "lat": i["countryInfo"]["lat"],
            "long": i["countryInfo"]["long"],
            "confirmed_cumulative": i["cases"],
            "confirmed_new": i["todayCases"],
            "deaths_cumulative": i["deaths"],
            "deaths_new": i["todayDeaths"],
            "recovered_cumulative": i["recovered"],
            "recovered_new": i["todayRecovered"],
            "active": i["active"],
            "critical": i["critical"],
            "updated": i["updated"],
            "continent": i["continent"],
            "flag": i["countryInfo"]["flag"],
        }
        for i in countries_updates
    ]

    countries_df = pd.DataFrame(countries, columns=countries[0].keys())

    if save:
        countries_df.to_csv("./data/countries.csv", index=False)

    return countries_df


def get_time_series(url=base_url, save=False):
    """
    Args:
        url (string, optional): common/home part of url used to derive other urls from which we get required information. Defaults to base_url
        save (bool, optional): arg determing whether the content gathered/updated should be saved or not. Defaults to False
    Returns:
        (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame): 4 timeseries, 1 global (all 3 combined into 1) and 3 country wise (segregated into confirmed, recovered and deaths) respectively
    """
    ts_base_url = url + "/historical"
    global_ts_url = ts_base_url + "/all?lastdays=all"

    global_ts_update = requests.get(global_ts_url).json()

    global_ts_df = pd.DataFrame(
        global_ts_update, columns=global_ts_update.keys()
    ).transpose()

    country_wise_ts_url = ts_base_url + "?lastdays=all"

    country_wise_ts = requests.get(country_wise_ts_url).json()

    ts_index = [i["country"] for i in country_wise_ts]

    country_confirmed = [i["timeline"]["cases"] for i in country_wise_ts]
    country_recovered = [i["timeline"]["recovered"] for i in country_wise_ts]
    country_deaths = [i["timeline"]["deaths"] for i in country_wise_ts]

    country_confirmed_df = pd.DataFrame(
        country_confirmed, columns=country_confirmed[0].keys(), index=ts_index
    )
    country_confirmed_df = country_confirmed_df.groupby(
        country_confirmed_df.index, as_index=True
    ).sum()

    country_deaths_df = pd.DataFrame(
        country_deaths, columns=country_deaths[0].keys(), index=ts_index
    )
    country_deaths_df = country_deaths_df.groupby(
        country_deaths_df.index, as_index=True
    ).sum()

    country_recovered_df = pd.DataFrame(
        country_recovered, columns=country_recovered[0].keys(), index=ts_index
    )
    country_recovered_df = country_recovered_df.groupby(
        country_recovered_df.index, as_index=True
    ).sum()

    global_ts_df["category"] = global_ts_df.index
    country_recovered_df["country"] = country_recovered_df.index
    country_deaths_df["country"] = country_deaths_df.index
    country_confirmed_df["country"] = country_confirmed_df.index

    if save:

        global_ts_df.to_csv("./data/global_ts.csv", index=False)
        country_confirmed_df.to_csv("./data/country_confirmed.csv", index=False)
        country_deaths_df.to_csv("./data/country_deaths.csv", index=False)
        country_recovered_df.to_csv("./data/country_recovered.csv", index=False)

    return global_ts_df, country_confirmed_df, country_deaths_df, country_recovered_df


def get_vaccination_update(url=base_url, save=False):

    """
    Args:
        url (string, optional): common/home part of url used to derive other urls from which we get required information. Defaults to base_url
        save (bool, optional): arg determing whether the content gathered/updated should be saved or not. Defaults to False
    Returns:
        (pd.DataFrame, pd.DataFrame): 2 dataframes for vaccination updates, globally and segregated country wise respectively
    """
    vaccine_base_url = url + "/vaccine/coverage"
    vaccine_global_url = vaccine_base_url + "?lastdays=all"
    vac_global_update = requests.get(vaccine_global_url).json()

    vac_global_df = pd.DataFrame(
        vac_global_update, columns=vac_global_update.keys(), index=[0]
    )

    vaccine_country_url = vaccine_base_url + "/countries?lastdays=all&fullData=false"
    vac_country_update = requests.get(vaccine_country_url).json()

    vac_index = [i["country"] for i in vac_country_update]
    vac_country_values = [i["timeline"] for i in vac_country_update]

    vac_country_df = pd.DataFrame(
        vac_country_values, columns=vac_country_values[0].keys(), index=vac_index
    )

    vac_country_df["country"] = vac_country_df.index

    if save:
        vac_global_df.to_csv("./data/vac_global.csv", index=False)
        vac_country_df.to_csv("./data/vac_country.csv", index=False)

    return vac_global_df, vac_country_df


def gen_covid_data_object():
    return


if __name__ == "__main__":

    global_update = get_global_update(save=True)
    continents_df = get_continent_update(save=True)
    countries_df = get_country_update(save=True)
    (
        global_ts_df,
        country_confirmed_df,
        country_deaths_df,
        country_recovered_df,
    ) = get_time_series(save=True)
    vac_global_df, vac_country_df = get_vaccination_update(save=True)

    # class Data:
    #     def __init__(self):
    #         self.global_update = global_update
    #         self.continents_df = continents_df
    #         self.countries_df = countries_df
    #         self.global_ts_df = global_ts_df
    #         self.country_confirmed_df = country_confirmed_df
    #         self.country_deaths_df = country_deaths_df
    #         self.country_recovered_df = country_recovered_df
    #         self.vac_global_df = vac_global_df
    #         self.vac_country_df = vac_country_df

    # covid_data = Data()

    # with open("./covid_data_object.pkl", "wb") as file:
    #     pickle.dump(covid_data, file)

