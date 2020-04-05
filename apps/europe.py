import dash_core_components as dcc
import dash_html_components as html
from app import colors, app
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import geopandas as gpd
import json
from dash.dependencies import Input, Output

ACCESS_TOKEN = "pk.eyJ1IjoiaGV0dGkiLCJhIjoiY2s4bGZkdnpxMDJ2ZjNncW9pY2R6NTVqdyJ9.XbSVnMxmb86c7hADyekrWA"

europe = pd.read_csv("./data_processing/europe/data_europe.csv")
gdf = gpd.GeoDataFrame(
    europe, geometry=gpd.points_from_xy(x=europe.Long_, y=europe.Lat)
)
gdf.to_file("europe.json", driver="GeoJSON")

with open("europe.json") as f:
    geojson = json.load(f)

col_map_fig = go.Figure(px.scatter_mapbox(gdf, lat=gdf["Lat"], lon=gdf["Long_"],
                                          color=gdf["Confirmed"],
                                          color_continuous_scale='Reds',
                                          hover_name=gdf["Country_Region"],
                                          hover_data=["Confirmed"],
                                          size=gdf["Confirmed"]))
col_map_fig.update_layout(mapbox_accesstoken=ACCESS_TOKEN, mapbox_zoom=2,
                          mapbox_center={"lat": 51.1657, "lon": 10.4515})
col_map_fig.layout.template = "plotly_dark"

col_map = dcc.Graph(
    id='example-graph-2',
    figure=col_map_fig
)

confirmed_europe = pd.read_csv('./data_processing/europe/act_confirmed_europe.csv').sort_values(by="Country/Region")
death_europe = pd.read_csv('./data_processing/europe/act_death_europe.csv').sort_values(by="Country/Region")

fig = go.Figure()
fig.layout.template = "plotly_dark"
fig.add_trace(go.Scatter(y=confirmed_europe.iloc[0, 46:], x=confirmed_europe.columns[46:],
                         marker_color="#08F7FE",
                         mode='markers',
                         name=confirmed_europe["Country/Region"].iloc[0]))
fig.add_trace(go.Scatter(y=confirmed_europe.iloc[1, 46:], x=confirmed_europe.columns[46:],
                         marker_color="#E8E500",
                         mode='markers',
                         name=confirmed_europe["Country/Region"].iloc[1]))
fig.add_trace(go.Scatter(y=confirmed_europe.iloc[2, 46:], x=confirmed_europe.columns[46:],
                         marker_color="#FE0000",
                         mode='markers',
                         name=confirmed_europe["Country/Region"].iloc[2]))
fig.add_trace(go.Scatter(y=confirmed_europe.iloc[3, 46:], x=confirmed_europe.columns[46:],
                         marker_color="#FFAA01",
                         mode='markers',
                         name=confirmed_europe["Country/Region"].iloc[3]))
fig.add_trace(go.Scatter(y=confirmed_europe.iloc[4, 46:], x=confirmed_europe.columns[46:],
                         marker_color="#B8FB3C",
                         mode='markers',
                         name=confirmed_europe["Country/Region"].iloc[4]))

death = go.Figure()
death.layout.template = "plotly_dark"
death.add_trace(go.Scatter(y=death_europe.iloc[0, 46:], x=death_europe.columns[46:],
                           marker_color="#08F7FE",
                           mode='markers',
                           name=death_europe["Country/Region"].iloc[0]))
death.add_trace(go.Scatter(y=death_europe.iloc[1, 46:], x=death_europe.columns[46:],
                           marker_color="#E8E500",
                           mode='markers',
                           name=death_europe["Country/Region"].iloc[1]))
death.add_trace(go.Scatter(y=death_europe.iloc[2, 46:], x=death_europe.columns[46:],
                           marker_color="#FE0000",
                           mode='markers',
                           name=death_europe["Country/Region"].iloc[2]))
death.add_trace(go.Scatter(y=death_europe.iloc[3, 46:], x=death_europe.columns[46:],
                           marker_color="#FFAA01",
                           mode='markers',
                           name=death_europe["Country/Region"].iloc[3]))
death.add_trace(go.Scatter(y=death_europe.iloc[4, 46:], x=death_europe.columns[46:],
                           marker_color="#B8FB3C",
                           mode='markers',
                           name=death_europe["Country/Region"].iloc[4]))

layout = html.Div([
    html.H1(children="Europe Dashboard", style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Link('Go to Home', href='/'),
    col_map,
    dcc.Tabs(id='tabs-example', value="tab-1", children=[
        dcc.Tab(label='Confirmed', value='tab-1', style={
            'textAlign': 'center',
            'color': colors['text'],
            'backgroundColor': '#121212',
        }, selected_style={
            'backgroundColor': '#ffae1a',
            'color': colors['text'],
        }),
        dcc.Tab(label='Death', value='tab-2', style={
            'textAlign': 'center',
            'color': colors['text'],
            'backgroundColor': '#121212',
        }, selected_style={
            'backgroundColor': '#ffae1a',
            'color': colors['text'],
        })
    ]),
    html.Div(id='tabs-example-content'),
])


@app.callback(Output('tabs-example-content', "children"),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            dcc.Graph(id='example-graph-1',
                      figure=fig)
        ])
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph(id='example-graph-2',
                      figure=death)
        ])
