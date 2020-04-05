import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import pandas as pd
import plotly.graph_objects as go
import geopandas as gpd
from shapely import wkt

server = flask.Flask('app')
app = dash.Dash('app', server=server)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

data = pd.read_csv("cleaned_data.csv")
data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y')
casesAusria = go.Scatter(
    x=data.date,
    y=data.cases,
    name="Austria",
    line=dict(color='#39ff14'),
    mode='lines+markers',
    opacity=0.8)

data = [casesAusria]

layout = dict(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'
    ),
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['background'],
    title={
        'text': "Corona Cases in Austria",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Date",
    yaxis_title="Confirmed Cases",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color=colors['text']
    )
)

fig = dict(data=data, layout=layout)

ACCESS_TOKEN = "pk.eyJ1IjoiaGV0dGkiLCJhIjoiY2s4bGZkdnpxMDJ2ZjNncW9pY2R6NTVqdyJ9.XbSVnMxmb86c7hADyekrWA"
europe_cases = pd.read_csv("cleaned_data_europe.csv")
europe_cases = europe_cases.dropna(how='all', axis=1)
data = dict(type='choropleth',
            locations=europe_cases["Country_Region"],
            locationmode='country names',
            colorscale='Reds',
            text=europe_cases["Country_Region"],
            z=europe_cases["Confirmed"],
            colorbar={'title': 'Confirmed Cases', 'len': 200, 'lenmode': 'pixels'},
            )
layout = dict(geo={'scope': 'europe'}, font=dict(
    family="Courier New, monospace",
    size=18,
    color=colors['text'])
              ,
              mapbox=dict(accesstoken=ACCESS_TOKEN,
                          bearing=10,
                          pitch=60,
                          zoom=1000,
                          style="satellite"),
              width=1200,
              height=800,
              title={
                  'text': "Europa Confirmed Cases",
                  'y': 0.9,
                  'x': 0.5,
                  'xanchor': 'center',
                  'yanchor': 'top'},
              )

df = pd.read_csv("austria_map.csv")
df['geometry'] = df['geometry'].apply(wkt.loads)
gdf = gpd.GeoDataFrame(df, geometry='geometry')
gdf.plot()
col_map = go.Figure(data=[data], layout=layout)

app.layout = html.Div(style={"background-color": colors['background']}, children=[
    dcc.Graph(id='austria_trend', figure=fig),
    dcc.Graph(id="europe_map", figure=col_map),
    dcc.Graph(id="austria_map", figure=gdf.plot(cmap="Reds", column="cases", legend=True))
])

if __name__ == '__main__':
    app.run_server(debug=True)

print("Application Deployed")
