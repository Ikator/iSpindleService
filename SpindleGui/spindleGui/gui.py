import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import time
import plotly.graph_objs as go
import spindleGui.data_components as dc
from flask import request 


app = dash.Dash('Spindle-Api')

app.title = 'iSpindle'

data_dict = {"DateTime":[],
    "Temperature": [],
    "Plato": [],
    "Angle": [],
    "Battery": []
    }

data = []

app.layout = html.Div([
    html.Div([
        dcc.Location(id='url', refresh=False),
        html.H2(id='title', title='iSpindle'),
        ]),
    dcc.Dropdown(id='spindle-data-names',
            options=[{'label': s, 'value': s}
                    for s in (list(data_dict.keys())[1:])],
            value=['Temperature', 'Plato'],
            multi=True
            ),
    html.Div(children=html.Div(id='graph')),
    dcc.Interval(
        id='graph-update',
        interval=60*1000),
    ])



[Input('graph-update', 'n_intervals')]
@app.callback(
    dash.dependencies.Output('graph','children'),
    [dash.dependencies.Input('graph-update', 'n_intervals'),
    dash.dependencies.Input('url', 'pathname'),
    dash.dependencies.Input('spindle-data-names', 'value')]
    )
def update_graph(interval, pathname, data_names):
    spindleName = dc.getSpindleName(pathname)
    if spindleName is None:
        return
    data = dc.updateData(spindleName)
    if data is None:
        return

    data_dict['DateTime'], data_dict['Temperature'], data_dict['Plato'], data_dict['Angle'], data_dict['Battery'] = dc.convertData(data)

    fig = go.Figure()

    for data_name in data_names:
        fig.add_trace(go.Scatter(
            x= data_dict['DateTime'],
            y= data_dict[data_name],
            name= data_name
            ))
    

    fig.update_layout(
        xaxis=dict(
            title="Date"
            )
    )

    graph = html.Div(dcc.Graph(
        id='plot',
        animate=True,
        figure= fig))


    return graph


@app.callback(dash.dependencies.Output('title', 'children'),
             [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    spindleName = dc.getSpindleName(pathname)
    if spindleName is not None:
        return spindleName
    return '404 balbla'

