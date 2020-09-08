
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app, update_view_object

view, path = update_view_object()

layout = html.Div(children=[
    dbc.Row(
        dbc.ButtonGroup([
            dbc.Button('Wordcloud', id='wordcloud-button',n_clicks=0),
            dbc.Button('Table', id='table-button', n_clicks=0),
            dbc.Button('Scaled', id='scaled-button', n_clicks=0),
            dbc.Button('Racing Bar', id='racing-bar-button', n_clicks=0),
            dbc.Button('Stacked', id='stacked-button', n_clicks=0)],
            size='lg'
        ),
        justify='center'

    ),
    dbc.Row(
        dbc.Col(
            html.Div([
                html.Br(),
                html.H3(id='title'),
                html.Div(id='alert-overview',style={'display':'none'},children=[dbc.Alert('This view are not available because data is missing.',color='info')]),
                html.Div(id='graph-overview-container',children=[dcc.Graph(id='graph')]),
                html.Br(),
                html.Br(),
                html.Div(id='image-overview-container',children=html.Img(src=app.get_asset_url(path[7:]+'corpus.png'),style={"width":'70%','height':'70%'}))
                
            ]),
            width={"size": 10}
        ),
        justify='center'
    )
    
])

@app.callback([Output('alert-overview','style'),Output('graph-overview-container','style'),Output('image-overview-container','style'),Output('graph', 'figure'),Output('title','children')],
              [Input('wordcloud-button','n_clicks'),Input('table-button','n_clicks'),Input('scaled-button', 'n_clicks'),Input('racing-bar-button', 'n_clicks'),Input('stacked-button', 'n_clicks')])

def update_view(btn1, btn2, btn3, btn4,btn5):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    display_image = {'display':'none'}
    display_alert = {'display':'none'}
    display_graph = {'display':'block'}
    if 'scaled-button' in changed_id:
        fig = view.scaled_topics()
        title = 'Scaled view'
    elif 'racing-bar-button' in changed_id:
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
    elif 'table-button' in changed_id:
        fig = view.table()
        title = 'Table view'
    else :
        display_graph = {'display':'none'}
        display_image = {'display':'block'}
        title = 'Wordcloud of the entire corpus'
        fig = view.scaled_topics()
    
    return display_alert,display_graph,display_image,fig,title

@app.callback([Output('store-id-overview','data'),Output('store-path-overview', 'data')],[Input('graph','clickData')])

def store_pathname_on_click(clickData):
    if clickData == None:
        raise PreventUpdate
    else:
        return str(clickData['points'][0]['pointNumber']),'/topic'

