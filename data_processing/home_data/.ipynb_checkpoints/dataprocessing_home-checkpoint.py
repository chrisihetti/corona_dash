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

df = pd.read_csv(url)
df_cleaned = df[["Country_Region","Confirmed","Deaths"]]
df_sum = df_cleaned.groupby("Country_Region").sum()

df_sum.to_csv("home_data.csv")
