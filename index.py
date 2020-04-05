from app import app, colors
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from apps import austria, europe, usa
import pandas as pd
import dash_table

df = pd.read_csv('./data_processing/home_data/home_data.csv')
table = dash_table.DataTable(
    id='deaths',
    columns=[{"name": i, "id": i} for i in df[["Country_Region", "Confirmed"]]],
    data=df.nlargest(15, 'Confirmed').to_dict('records'),
    style_as_list_view=True,
    sort_action="native",
    sort_mode="single",
    style_header={'backgroundColor': '#121212', 'border': '1px solid white'},
    style_table={
        "maxWidth": "300px",
    },
    style_data={'border': '1px solid white'},
    style_data_conditional=[
        {'if': {'column_id': 'Country_Region'},
         'width': '60%'},
        {'if': {'column_id': 'Confirmed'},
         'width': '40%'}
    ],
    style_cell={
        'backgroundColor': '#121212',
        'color': 'white',
        'textAlign': 'center'
    },
)
overview = dash_table.DataTable(
    id='deaths',
    columns=[{"name": i, "id": i} for i in df[["Country_Region", "Deaths"]]],
    data=df.nlargest(15, 'Deaths').to_dict('records'),
    style_as_list_view=True,
    sort_action="native",
    sort_mode="single",
    style_header={'backgroundColor': '#121212', 'border': '1px solid white'},
    style_table={
        "maxWidth": "300px",
    },
    style_data={'border': '1px solid white'},
    style_data_conditional=[
        {'if': {'column_id': 'Country_Region'},
         'width': '60%'},
        {'if': {'column_id': 'Deaths'},
         'width': '40%'}
    ],
    style_cell={
        'backgroundColor': '#121212',
        'color': 'white',
        'textAlign': 'center'
    },
)

layout = html.Div(children=[
    html.H1(children="Covid 19 Dashboard", style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div(children=[
        dcc.Link([
            "Austria"
        ], id="austriaPage", href="/austria", className="set of classnames", style={
            'textAlign': 'center',
            'color': colors['text'],
            'marginRight': '4em'
        }),
        dcc.Link([
            "Europe"
        ], id="europePage", href="/europe", className="set of classnames", style={
            'textAlign': 'center',
            'color': colors['text'],
            'marginRight': '4em'
        }),
        dcc.Link([
            "USA"
        ], id="usaPage", href="/usa", className="set of classnames", style={
            'textAlign': 'center',
            'color': colors['text']
        })
    ]),
    html.Br(),


    html.Div(children=[
        html.Div([table], style={'width': '25%', 'display': 'inline-block',
                                 'margin-left': '1em'}),
        html.Div([
            html.Br(),
            html.Br(),
            html.Img(src=app.get_asset_url('home.png'), style={
                'height': '100%',
                'width': '100%'
            })], style={'width': '40%', 'display': 'inline-block'
                        }),
        html.Div([overview],
                 style={'width': '25%', 'display': 'inline-block', 'margin-left': '4em'})
    ]),
])

app.layout = html.Div(style={'textAlign': 'center'},
                      children=[
                          dcc.Location(id='url', refresh=False),
                          html.Div(id='page-content')])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/austria':
        return austria.layout
    elif pathname == '/europe':
        return europe.layout
    elif pathname == "/usa":
        return usa.layout
    else:
        return layout


if __name__ == '__main__':
    app.run_server(debug=True)
