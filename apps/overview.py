
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app,view

layout = html.Div(children=[
    html.Button('Scaled', id='scaled-button', n_clicks=0),
    html.Button('Racing Bar', id='racing-bar-button', n_clicks=0),
    html.Button('Stacked', id='stacked-button', n_clicks=0),
    html.Div([
        html.H3(id='title'),
        dcc.Graph(id='graph')
    ])
])

@app.callback([Output('graph', 'figure'),Output('title','children')],
              [Input('scaled-button', 'n_clicks'),
               Input('racing-bar-button', 'n_clicks'),
               Input('stacked-button', 'n_clicks')])

def update_view(btn1, btn2, btn3):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'racing-bar-button' in changed_id:
        fig = view.racing_bar_graph()
        title = 'Racing Bar view'
    elif 'stacked-button' in changed_id:
        fig = view.streamgraph()
        title = 'Stacked view'
    else:
        fig = view.scaled_topics()
        title = 'Scaled view'
    return fig,title

@app.callback([Output('store-nb','data'),Output('store-path', 'data')],[Input('graph','clickData')])

def store_pathname_on_click(clickData):
    if clickData == None:
        raise PreventUpdate
    else:
        return str(clickData['points'][0]['pointNumber']),'/topic'

