import dash_core_components as dcc
import dash_html_components as html
from app import colors

layout = html.Div([
    html.H1(children="Europe Dashboard", style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Link('Go to Home', href='/')
])
