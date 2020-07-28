

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app,view

layout = html.Div(children=[
    dcc.Link(
        html.Button("overview"),
        href='/'),
    dcc.Link(
        html.Button("topic"),
        href='/topic'),
    html.H1(children='Topics Explorer'),
    html.Div([
        html.Div([
            html.H3('Scaled view'),
            dcc.Graph(
                id='scaled',
                figure=view.scaled_topics())
        ],className="six columns"),
        html.Div([
            html.H3('Topics evolution over years'),
            dcc.Graph(
                id='racing-bar-graph',
                figure=view.racing_bar_graph())
        ],className="six columns"),
    ], className="row"),
    html.Div([
        html.H3('Stacked view'),
        dcc.Graph(
            id='streamgraph',
            figure=view.streamgraph()) 
    ]),
    dcc.Store(id='topic-id',storage_type="session")  
])

@app.callback([Output('url','search'),Output('url', 'pathname')],[Input('scaled','clickData')])

def update_pathname(clickData):
    if clickData == None:
        raise PreventUpdate
    return str(clickData['points'][0]['pointNumber']),'/topic'

