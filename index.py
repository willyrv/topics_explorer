import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from app import app,view
from apps import overview, topic, dictionary, doc, word, select_corpus
import input

from navbar import Navbar

nav = Navbar()


app.layout = dbc.Container(
    html.Div([
        nav,
        dcc.Location(id='url',refresh=False),
        html.Br(),
        html.Div(id='page-content'),
        dcc.Store(id='store-id-overview',storage_type='session',clear_data=True),
        dcc.Store(id='store-path-overview',storage_type='session',clear_data=True),
        dcc.Store(id='store-id-topic-doc',storage_type='session',clear_data=True),
        dcc.Store(id='store-id-topic-word',storage_type='session',clear_data=True),
        dcc.Store(id='store-path-topic',storage_type='session',clear_data=True),
        dcc.Store(id='store-id-word',storage_type='session',clear_data=True),
        dcc.Store(id='store-path-word',storage_type='session',clear_data=True),
        dcc.Store(id='store-id-doc',storage_type='session',clear_data=True),
        dcc.Store(id='store-path-doc',storage_type='session',clear_data=True),
        dcc.Store(id='store-path-select-corpus',storage_type='session',clear_data=True),
    ]),
    fluid=True
)
inputs_index = [Input(str(id),'n_clicks') for id in range(view.model.number_topics)]
inputs_index.insert(0,Input('store-id-overview','data'))
inputs_index.insert(1,Input('store-path-overview','data'))
inputs_index.insert(2,Input('store-path-topic','data'))
inputs_index.insert(3,Input('store-id-word','data'))
inputs_index.insert(4,Input('store-path-word','data'))
inputs_index.insert(5,Input('store-id-doc','data'))
inputs_index.insert(6,Input('store-path-doc','data'))
inputs_index.insert(7,Input('store-path-select-corpus','data'))


@app.callback([Output('url','search'),Output('url','pathname')],inputs_index)

def update_pathname(store_id_overview,store_path_overview,store_path_topic,store_id_word,store_path_word,store_id_doc,store_path_doc,store_path_select_corpus,*args):
    ctx = dash.callback_context
    c = ctx.triggered[0]['prop_id'].split('.')[0]
    if not ctx.triggered or ((c =='store-id-overview' or c =='store-path-overview') and store_id_overview==None) or ((c =='store-id-word' or c =='store-path-word') and store_id_word==None) or ((c =='store-id-doc' or c =='store-path-doc') and store_id_doc==None) or (c =='store-path-select-corpus' and store_path_select_corpus==None):
        raise PreventUpdate
    elif  c =='store-id-overview' or c =='store-path-overview':
        return store_id_overview, store_path_overview
    elif  c =='store-id-word' or c =='store-path-word':
        return store_id_word, store_path_word
    elif  c =='store-id-doc' or c =='store-path-doc':
        return store_id_doc, store_path_doc
    elif  c =='store-path-select-corpus':
        return '', store_path_select_corpus
    elif  c =='store-path-topic':
        return '', store_path_topic
    else:
        return str(c),'/topic'


@app.callback(Output('page-content', 'children'),[Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return select_corpus.layout
    if pathname == '/overview':
        return overview.layout
    elif '/topic' in pathname:
        return topic.layout
    elif pathname == '/dictionary':
        return dictionary.layout
    elif pathname == '/doc':
        return doc.layout
    elif pathname == '/word':
        return word.layout
    elif pathname == '/upload':
        return input.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)