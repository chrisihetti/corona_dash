import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import pandas as pd
import plotly.graph_objects as go

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

# Now here's the Dash part:

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    dcc.Graph(id='my-graph', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)

print("Application Deployed")
