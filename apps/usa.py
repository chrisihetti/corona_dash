import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import dash_table
from app import colors
from urllib.request import urlopen
import json

ACCESS_TOKEN = "pk.eyJ1IjoiaGV0dGkiLCJhIjoiY2s4bGZkdnpxMDJ2ZjNncW9pY2R6NTVqdyJ9.XbSVnMxmb86c7hADyekrWA"

confirmed_usa = pd.read_csv('./data_processing/usa/confirmed_usa.csv')
death_usa = pd.read_csv('./data_processing/usa/death_usa.csv')
actual_usa = pd.read_csv('./data_processing/usa/actual_usa.csv')
groupData = actual_usa.groupby("Country_Region").sum()
text = 'Total Confirmed: ' + str(groupData["Confirmed"][0]) + '\t Total Death: ' + str(
    groupData["Deaths"][0]) + '\n Death Ratio: ' + format(
    (((groupData["Deaths"][0]) / (groupData["Confirmed"][0])) * 100), '.2f') + "%"
table = dash_table.DataTable(
    id='deaths',
    columns=[{"name": i, "id": i} for i in actual_usa[["Admin2", "Confirmed", "Deaths"]]],
    data=actual_usa.nlargest(15, 'Deaths').to_dict('records'),
    style_as_list_view=True,
    sort_action="native",
    sort_mode="single",
    style_header={'backgroundColor': '#121212', 'border': '1px solid white'},
    style_table={
        "maxWidth": "250px",
    },
    style_data={'border': '1px solid white'},
    style_cell={
        'backgroundColor': '#121212',
        'color': 'white',
        'textAlign': 'center'
    },
)

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

actual_usa["text"] = "Confirmed : " + actual_usa["Confirmed"].astype(str) + " City: " + actual_usa[
    "Admin2"].astype(str)
map = go.Figure(go.Choroplethmapbox(geojson=counties, locations=actual_usa["FIPS"],
                                    z=actual_usa["Confirmed"], zmin=0, zmax=10000,
                                    colorscale='Reds', text=actual_usa["text"]))
map.update_layout(mapbox_accesstoken=ACCESS_TOKEN, mapbox_zoom=3,
                  mapbox_center={"lat": 37.0902, "lon": -95.7129})
map.layout.template = "plotly_dark"
colorMap = dcc.Graph(
    id='example-graph-2',
    figure=map
)

fig = go.Figure()
fig.layout.template = "plotly_dark"
fig.add_trace(go.Scatter(y=death_usa["US"], x=death_usa['Unnamed: 0'],
                         marker_color="#ff073a",
                         mode='lines+markers',
                         name='Death'))
fig.add_trace(
    go.Scatter(y=confirmed_usa["US"], x=confirmed_usa['Unnamed: 0'],
               marker_color="#4deeea",
               mode='lines+markers',
               name='Confirmed'))
daily_trend = dcc.Graph(
    id='example-graph-2',
    figure=fig
)

layout = html.Div([
    html.H1(children="USA Dashboard", style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Link('Go to Home', href='/'),
    html.Br(),
    dcc.Textarea(
        value=text,
        style={'width': '30%', 'color': colors['text'], 'backgroundColor': '#121212',
               "font-size": "18px", 'float': 'left'},
        contentEditable=False
    ),
    html.Br(),
    html.Br(),
    html.Div(children=[
        html.Div([table], style={'display': 'inline-block', 'width': '33%', 'float': 'left', 'margin-left': '4em'}),
        html.Div([daily_trend], style={'display': 'inline-block', 'width': '60%'
                                       })
    ], style={'width': '100%', 'display': 'inline-block'}),
    html.Br(),
    colorMap
])
