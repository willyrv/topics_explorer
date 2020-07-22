

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
    ], className="row")   
])

@app.callback(
    Output('link','href'),
    [Input('figure','hoverData')])

def display_hover_data(hoverData):
    if hoverData:
        target = hoverData['points'][0]['customdata']
        return target
    else :
        raise PreventUpdate



