##########################################################
# COVID-19 Data Manipulation and Prediction Experiment   #
# Alex Wojtowicz                                         #
# alex.wojtowicz@gmail.com                               #
##########################################################

import pandas as pd
import math

# Set options for pandas display
pd.set_option('display.max_columns', 30)
pd.set_option('display.max_rows', 1000)
cases = pd.read_csv('data/time_series_covid19_confirmed_global_narrow.csv', skiprows=[1])
deaths = pd.read_csv('data/time_series_covid19_deaths_global_narrow.csv', skiprows=[1])

##########################################################
# Feature Engineering
##########################################################

cases = cases.rename(columns={'Value':'total_cases'})
cases['new_cases'] = ''
cases['total_deaths'] = ''
cases['new_deaths'] = ''

number_of_days = len(cases["Date"].unique())
total_rows = len(cases)
row = 0
country_reset_flag = 0

# variables
cases_today = ''
cases_yesterday = ''
deaths_today = ''
deaths_yesterday = ''
new_cases = ''
new_deaths = ''
stopper = 1

for i in range(total_rows):
    province = cases.iloc[i,0]
    country = cases.iloc[i,1]
    lat = cases.iloc[i,2]
    lon = cases.iloc[i,3]
    date = cases.iloc[i, 4]
    cases_today = cases.iloc[i, 5]
    deaths_today = deaths.iloc[i, 5]
    country_reset_flag = math.floor(stopper / number_of_days)

    if(country_reset_flag == 1):
        stopper = 0
        cases_yesterday = cases_today
        deaths_yesterday = deaths_today

    if(country_reset_flag == 0):
        cases_yesterday = cases.iloc[i + 1, 5]
        deaths_yesterday = deaths.iloc[i + 1, 5]

    new_cases = cases_today - cases_yesterday
    new_deaths = deaths_today - deaths_yesterday
    cases.at[i, "new_cases"] = new_cases
    cases.at[i, "new_deaths"] = new_deaths
    cases.at[i, "total_deaths"] = deaths_today
    stopper += 1


print(cases)