
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app,view

layout = html.Div(children=[
    dbc.ButtonGroup([
        dbc.Button('Scaled', id='scaled-button', n_clicks=0),
        dbc.Button('Racing Bar', id='racing-bar-button', n_clicks=0),
        dbc.Button('Stacked', id='stacked-button', n_clicks=0)
    ],
    size = 'lg'
    ),
    dbc.Row(
        dbc.Col(
            html.Div([
                html.Br(),
                html.H3(id='title'),
                html.Div(id='alert-overview',style={'display':'none'},children=[dbc.Alert('This view are not available because data is missing.',color='info')]),
                html.Div(id='graph-overview-container',children=[dcc.Graph(id='graph')])
                
            ]),
            width={"size": 8, "offset": 1}
        )
    )
    
])

@app.callback([Output('alert-overview','style'),Output('graph-overview-container','style'),Output('graph', 'figure'),Output('title','children')],
              [Input('scaled-button', 'n_clicks'),
               Input('racing-bar-button', 'n_clicks'),
               Input('stacked-button', 'n_clicks')])

def update_view(btn1, btn2, btn3):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    display_alert = {'display':'none'}
    display_graph = {'display':'block'}
    if 'racing-bar-button' in changed_id:
        if view.model.corpus.dates==False:
            display_alert = {'display':'block'}
            display_graph = {'display':'none'}
            fig= view.scaled_topics()
        else:
            fig = view.racing_bar_graph()
        title = 'Racing Bar view'
    elif 'stacked-button' in changed_id:
        if view.model.corpus.dates==False:
            display_alert = {'display':'block'}
            display_graph = {'display':'none'}
            fig = view.scaled_topics()
        else:
            fig = view.streamgraph()
        title = 'Stacked view'
    else:
        fig = view.scaled_topics()
        title = 'Scaled view'
    return display_alert,display_graph,fig,title

@app.callback([Output('store-nb','data'),Output('store-path', 'data')],[Input('graph','clickData')])

def store_pathname_on_click(clickData):
    if clickData == None:
        raise PreventUpdate
    else:
        return str(clickData['points'][0]['pointNumber']),'/topic'

