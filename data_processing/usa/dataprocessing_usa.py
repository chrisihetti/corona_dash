import requests
import urllib
import datetime
from datetime import timedelta
import io
from bs4 import BeautifulSoup
import pandas as pd

from datetime import date
today = date.today()
csvname = today.strftime('%m-%d-%Y')+".csv"
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+csvname

req = requests.get(url)
if(req.status_code == 404):
    today = today - timedelta(days = 1)
    csvname = today.strftime('%m-%d-%Y')+".csv"
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+csvname
    req = requests.get(url)

req = requests.get(url)
if(req.status_code == 404):
    today = today - timedelta(days = 1)
    csvname = today.strftime('%m-%d-%Y')+".csv"
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+csvname
    req = requests.get(url)

all_countries = pd.read_csv(url)
us_actual = all_countries[all_countries["Country_Region"] == "US"]
us_actual = us_actual.dropna()

us_actual.to_csv("actual_usa.csv",index = False)

us_actual[us_actual["Province_State"]=="New York"]

confirmed_usa = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
death_usa = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv")

confirmed_usa = confirmed_usa.groupby("Country_Region").sum().iloc[:, 5:].loc["US"]
confirmed_usa.to_csv("confirmed_usa.csv")

death_usa = death_usa.groupby("Country_Region").sum().iloc[:, 6:].loc["US"]
death_usa.to_csv("death_usa.csv")
