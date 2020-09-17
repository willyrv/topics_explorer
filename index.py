import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from app import app, update_view_object
from apps import overview, topic, dictionary, doc, word, select_corpus
import input

from navbar import Navbar


view = update_view_object()[0]

app.layout = dbc.Container(
    html.Div([
        html.Div(id='navbar'),
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
        dcc.Store(id='store-id-doc-word',storage_type='session',clear_data=True),
        dcc.Store(id='previous-view',storage_type='session',clear_data=True)
        
        
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


@app.callback([Output('url','search'),Output('url','pathname'),Output('store-id-doc-word','data'),Output('previous-view','data')],inputs_index)

def update_pathname(store_id_overview,store_path_overview,store_path_topic,store_id_word,store_path_word,store_id_doc,store_path_doc,store_path_select_corpus,*args):

    '''Method in a callback whose goal is to update the url after a click event triggered by the user. It works with some Store dash components which permits to save the context of the click event.'''

    ctx = dash.callback_context
    c = ctx.triggered[0]['prop_id'].split('.')[0]
    if not ctx.triggered or ((c =='store-id-overview' or c =='store-path-overview') and store_id_overview==None) or (c =='store-id-word' or c =='store-path-word') and (store_id_word==None) or ((c =='store-id-doc' or c =='store-path-doc') and store_id_doc==None) or (c =='store-path-select-corpus' and store_path_select_corpus==None):
        raise PreventUpdate
    elif  c =='store-id-overview' or c =='store-path-overview':
        return store_id_overview, store_path_overview,'','overview'
    elif  c =='store-id-word' or c =='store-path-word':
        if store_path_word =='/doc':
            return '',store_path_word,store_id_word,'word'
        else:
            return store_id_word, store_path_word,'','word'
    elif  c =='store-id-doc' or c =='store-path-doc':
        return store_id_doc, store_path_doc,'','doc'
    elif  c =='store-path-select-corpus':
        return '', store_path_select_corpus,'','select-corpus'
    elif  c =='store-path-topic':
        return '', store_path_topic,'','topic'
    else:
        return str(c),'/topic','','unknown'


@app.callback([Output('page-content', 'children'),Output('navbar','children')],[Input('url', 'pathname')])

def display_page(pathname):

    '''Method in a callback which permits to display the page corresponding to the url'''
    
    view = update_view_object()[0]
    layout = '404'
    if pathname == '/':
        layout = select_corpus.layout
    if pathname == '/overview':
        layout = overview.layout
    elif '/topic' in pathname:
        layout = topic.topic_layout(view)
    elif pathname == '/dictionary':
        layout = dictionary.dictionary_layout(view)
    elif pathname == '/doc':
        layout = doc.doc_layout(view)
    elif pathname == '/word':
        layout = word.word_layout(view)
    elif pathname == '/upload':
        layout = input.layout
    return layout, Navbar(view)


if __name__ == '__main__':
    app.run_server(debug=False)