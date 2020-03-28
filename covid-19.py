##########################################################
# COVID-19 Data Manipulation and Prediction Experiment   #
# Alex Wojtowicz                                         #
# alex.wojtowicz@gmail.com                               #
##########################################################

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns

cases = pd.read_csv('data/time_series_covid19_confirmed_global_narrow.csv', skiprows=[1])
deaths = pd.read_csv('data/time_series_covid19_deaths_global_narrow.csv')

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

for country in countries:
    if(country != "United Kingdom"):
        number_of_days = len(cases[cases["Country/Region"] == country])
        new_cases = 0

        for day in range(number_of_days):
            total_cases_today = cases.iloc[day, 5]

            if(day == 65):
                total_cases_yesterday = total_cases_today
            if (day < 65):
                total_cases_yesterday = cases.iloc[day+1, 5]

            new_cases = total_cases_today - total_cases_yesterday
            cases.at[day, 'new_cases'] = new_cases


print(cases)