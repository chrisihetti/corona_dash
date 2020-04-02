import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import pandas_datareader.data as web

server = flask.Flask('app')
app = dash.Dash('app', server=server)

tickers = ['AAPL', 'MSFT', '^GSPC']
# We would like all available data from 01/01/2000 until 12/31/2016.
start_date = '2000-01-01'
end_date = '2020-04-01'
# User pandas_reader.data.DataReader to load the desired data. As simple as that.
panel_data = web.get_data_yahoo(tickers, start_date, end_date)
print(panel_data.head(5))

app.layout = html.Div([
    html.H1('Stock Tickers'),
    dcc.Graph(
        id='example',
        figure={
            'data': [
                {'x': list(panel_data["High"]["AAPL"].index.values), 'y': list(panel_data["High"]["AAPL"]), 'type': 'line', 'name': 'APPL'},
                {'x': list(panel_data["High"]["MSFT"].index.values), 'y': list(panel_data["High"]["MSFT"]), 'type': 'line', 'name': 'MSFT'},
                {'x': list(panel_data["High"]["^GSPC"].index.values), 'y': list(panel_data["High"]["^GSPC"]), 'type': 'line', 'name': '^GSPC'},
            ],
            'layout': {
                'title': 'Basic Dash Example'
            }
        }
    )
]
)

app.run_server()