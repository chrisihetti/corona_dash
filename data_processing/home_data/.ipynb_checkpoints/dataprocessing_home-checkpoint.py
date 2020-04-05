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

df_sum.to_csv("home_data.csv",index = True)

req = requests.get("https://simple.wikipedia.org/wiki/List_of_European_countries")
soup = BeautifulSoup(req.content, 'html.parser')
european_countries = []
for ele in soup.findAll("td"):
    if "title=" in str(ele).strip() and ele.text.startswith(" "):
        if "[" in ele.text.strip():
            european_countries.append(ele.text[0:len(ele.text)-5].strip())
        else: 
            european_countries.append(ele.text.lstrip().replace("\n",""))

european_countries

europe = df[df["Country_Region"].isin(european_countries)]

europe = europe[europe["Province_State"] == ""]

europe.to_csv("cleaned_data_europe.csv",index = False)
