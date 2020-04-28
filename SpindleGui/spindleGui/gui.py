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

data = []

app.layout = html.Div([
    html.Div([
        dcc.Location(id='url', refresh=False),
        html.H2(id='title', title='iSpindle'),
        ]),
    html.Div(children=html.Div(id='graph')),
    dcc.Interval(
        id='graph-update',
        interval=10*1000),
    ])



[Input('graph-update', 'n_intervals')]
@app.callback(
    dash.dependencies.Output('graph','children'),
    [dash.dependencies.Input('graph-update', 'n_intervals'),
    dash.dependencies.Input('url', 'pathname')]
    )
def update_graph(interval, pathname):
    spindleName = dc.getSpindleName(pathname)
    if spindleName is None:
        return
    data = dc.updateData(spindleName)
    if data is None:
        return

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dc.convertData(data,'datetime'),
        y=dc.convertData(data,'temperature'),
        name="Temperature"
        ))
    fig.add_trace(go.Scatter(
        x=dc.convertData(data,'datetime') ,
        y=dc.convertData(data,'gravity'),
        name="°Plato",
        yaxis="y2"
        ))

    fig.update_layout(
        xaxis=dict(
            title="Date"
        ),
        yaxis=dict(
            title="Temperature",
            range=[-1,30],
            titlefont=dict(
                color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            )
        ),
        yaxis2=dict(
            title="Plato",
            range=[30,-1],
            titlefont=dict(
                color="#ff7f0e"
            ),
            tickfont=dict(
                color="#ff7f0e"
            ),
            anchor="x",
            overlaying="y",
            side="right"
        )
    )
    fig.update_layout(
        title_text="iSpindle for " + spindleName,
        width = 800,
        height = 500
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
        return 'iSpindle for ' + spindleName
    return 'iSpindle'

