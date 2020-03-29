##########################################################
# COVID-19 Data Manipulation and Prediction Experiment   #
# Alex Wojtowicz                                         #
# alex.wojtowicz@gmail.com                               #
##########################################################

import pandas as pd

cases = pd.read_csv('data/time_series_covid19_confirmed_global_narrow.csv', skiprows=[1])
deaths = pd.read_csv('data/time_series_covid19_deaths_global_narrow.csv')

# Function to check if country is divided into provinces

def has_provinces(country):
    select_country = cases['Country/Region'] == country
    select_provinces = cases['Province/State']
    province_checker = cases[select_country & select_provinces]
    return province_checker['Province/State']

def new_cases(country):
    select_country = cases['Country/Region'] == country
    case_results = cases[select_country]
    number_of_days = len(case_results[case_results["Country/Region"] == country])
    for day in range(number_of_days):
        total_cases_today = case_results.iloc[day, 5]
        total_cases_today = int(total_cases_today)
        if (day == 65):
            total_cases_yesterday = int(total_cases_today)
        if (day < 65):
            total_cases_yesterday = case_results.iloc[day + 1, 5]
        new_cases = int(total_cases_today) - int(total_cases_yesterday)
        case_results.at[day, 'new_cases'] = new_cases


def new_cases_provinces(province):
    select_provinces = cases['Province/State'] == province
    province_results = cases[select_provinces]
    number_of_days = len(cases[cases["Province/State"] == province])
    new_cases = 0
    for day in range(number_of_days):
        total_cases_today = province_results.iloc[day, 5]
        if (day == 65):
            total_cases_yesterday = int(total_cases_today)
        if (day < 65):
            total_cases_yesterday = province_results.iloc[day + 1, 5]

        new_cases = int(total_cases_today) - int(total_cases_yesterday)
        province_results.at[day, 'new_cases'] = new_cases

##########################################################
# Data Cleaning
##########################################################

##########################################################
# Feature Engineering
##########################################################
# country_value = cases[["Country/Region", "Value"]]
# brazil = cases[cases["Country/Region"] == "Brazil"]

countries = cases["Country/Region"].unique()
cases['new_cases'] = ''
cases['total_deaths'] = ''
cases['new_deaths'] = ''


# Calculate new cases per day
for country in countries:

    # Check if country has provinces
    province_checker = has_provinces(country)

    # If there are no provinces, let's calculate new cases per day for that country
    if(len(province_checker) == 0):
        new_cases(country)

    # If there are provinces, let's calculate new cases per day for all provinces in that country
    if(len(province_checker) > 0 ):
        select_country = cases['Country/Region'] == country
        select_provinces = cases['Province/State']
        provinces = cases[select_country & select_provinces]
        unique_provinces = provinces['Province/State'].unique()
        for provinces in unique_provinces:
            new_cases_provinces(provinces)


# Aggregate deaths and deaths per day into cases dataframe


