import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from app import app,view
from apps import overview, topic, dictionary, doc, word

from navbar import Navbar

nav = Navbar()


app.layout = dbc.Container(
    html.Div([
        nav,
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
        dcc.Store(id='store-id-overview',storage_type='session',clear_data=True),
        dcc.Store(id='store-path-overview',storage_type='session',clear_data=True),
        dcc.Store(id='store-id-topic',storage_type='session',clear_data=True),
        dcc.Store(id='store-path-topic',storage_type='session',clear_data=True)
    ]),
    fluid=True
)
inputs_index = [Input(str(id),'n_clicks') for id in range(view.model.number_topics)]
inputs_index.insert(0,Input('store-id-overview','data'))
inputs_index.insert(1,Input('store-path-overview','data'))
inputs_index.insert(2,Input('store-path-topic','data'))

@app.callback([Output('url','search'),Output('url','pathname')],inputs_index)

def update_pathname(store_id_overview,store_path_overview,store_path_topic,*args):
    ctx = dash.callback_context
    if (not ctx.triggered or ctx.triggered[0]['prop_id'].split('.')[0]=='store-id-overview' or ctx.triggered[0]['prop_id'].split('.')[0]=='store-path-overview') and store_id_overview==None :
        raise PreventUpdate
    elif  ctx.triggered[0]['prop_id'].split('.')[0]=='store-id-overview' or ctx.triggered[0]['prop_id'].split('.')[0]=='store-path-overview':
        return store_id_overview, store_path_overview
    elif  ctx.triggered[0]['prop_id'].split('.')[0]=='store-path-topic':
        return '', store_path_topic
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        return str(button_id),'/topic'


@app.callback(Output('page-content', 'children'),[Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return overview.layout
    elif pathname == '/topic':
        return topic.layout
    elif pathname == '/dictionary':
        return dictionary.layout
    elif pathname == '/doc':
        return doc.layout
    elif pathname == '/word':
        return word.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)