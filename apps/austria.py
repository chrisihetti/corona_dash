import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from app import colors
import plotly.express as px
import geopandas as gpd

ACCESS_TOKEN = "pk.eyJ1IjoiaGV0dGkiLCJhIjoiY2s4bGZkdnpxMDJ2ZjNncW9pY2R6NTVqdyJ9.XbSVnMxmb86c7hADyekrWA"

confirmed_austria = pd.read_csv('./data_processing/austria/austria_confirmed.csv')
death_austria = pd.read_csv('./data_processing/austria/austria_death.csv')
austria_gdp = pd.read_csv("./data_processing/austria/austria_gdf.csv")
gdf = gpd.GeoDataFrame(
    austria_gdp, geometry=gpd.points_from_xy(x=austria_gdp.x, y=austria_gdp.y)
)

col_map_fig = go.Figure(px.scatter_mapbox(gdf, lon=gdf["x"], lat=gdf["y"],
                                          color=gdf["cases"],
                                          color_continuous_scale='Reds',
                                          hover_name=gdf["name"],
                                          hover_data=["cases"],
                                          size=gdf["cases"]))
col_map_fig.update_layout(mapbox_accesstoken=ACCESS_TOKEN, mapbox_zoom=5,
                          mapbox_center={"lat": 47.5162, "lon": 14.5501})
col_map_fig.layout.template = "plotly_dark"

col_map = dcc.Graph(
    id='example-graph-2',
    figure=col_map_fig
)
fig = go.Figure()
fig.layout.template = "plotly_dark"
fig.add_trace(
    go.Scatter(x=confirmed_austria["date"], y=confirmed_austria['cases'],
               marker_color="#4deeea",
               mode='lines+markers',
               name='Confirmed'))
fig.add_trace(go.Scatter(y=death_austria.iloc[0], x=death_austria.columns,
                         marker_color="#ff073a",
                         mode='lines+markers',
                         name='Death'))
daily_trend = dcc.Graph(
    id='graph1',
    figure=fig
)

layout = html.Div([
    html.H1(children="Austria Dashboard", style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Link('Go to Home', href='/'),
    daily_trend,
    col_map
])
