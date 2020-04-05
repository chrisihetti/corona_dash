import dash
import dash_bootstrap_components as dbc

colors = {"background": "#121212", "text": "#7FDBFF"}

app = dash.Dash('Example', external_stylesheets=[dbc.themes.DARKLY])
app.config['suppress_callback_exceptions'] = True
server = app.server
