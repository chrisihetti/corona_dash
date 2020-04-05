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
url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports/"+csvname

req = requests.get(url)
if(req.status_code == 404):
    today = today - timedelta(days = 1)
    csvname = today.strftime('%m-%d-%Y')+".csv"
    url = "https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports/"+csvname
    req = requests.get(url)

soup = BeautifulSoup(req.content, 'html.parser')

table = soup.find("table")

soup = BeautifulSoup(str(table.findAll("th")))
text = soup.get_text().replace(','," ")
column_names = [name for name in text.strip().split(" ") if len(name) > 0]

table_body = table.find('tbody')

rows = table_body.find_all('tr')

data = []
for row in rows:
    cols = row.findAll('td')
    data.append([ele.text.strip() for ele in cols if not 'class="blob-num' in str(ele)])

df = pd.DataFrame(data, columns=column_names)

df.to_csv("cleaned_data_world.csv",index = False)

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
