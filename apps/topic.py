import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate
import copy

from app import app,view,available_topics

nb_words = 50
nb_max_docs = view.model.max_number_docs()

layout = html.Div(children=[
    dcc.Store(id='store-top-words',storage_type='session',clear_data=True),
    dcc.Store(id='store-docs-topic',storage_type='session',clear_data=True),

    dbc.Row(dbc.Col(html.Div([
                html.Br(),
                html.H3(id='title-topic')]),
                width={'offset':1})),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.Br(),
                html.H5("Top words"),
                dbc.ListGroup([dbc.ListGroupItem(id='word'+str(w)) for w in range(nb_words)])
            ]),
            width={"size": 3, "offset": 1}
        ),
        dbc.Col([
            html.H5('Topic frequency evolution'),
            html.Div(id='graph-frequency-container',children=[dcc.Graph(id='frequency-per-years')]),
            html.H5('Related documents'),
            html.Ul([html.Div(id = 'doc' + str(doc)) for doc in range(nb_max_docs)]),
        ])
    ])
])

outputs_topic = [Output('word'+str(w),'children') for w in range(nb_words)] + [Output('doc'+str(doc),'children') for doc in range(nb_max_docs)] + [Output('doc'+str(doc),'style') for doc in range(view.model.max_number_docs())]
outputs_topic.insert(0,Output('title-topic','children'))
outputs_topic.append(Output('graph-frequency-container','style'))
outputs_topic.append(Output('frequency-per-years','figure'))
outputs_topic.append(Output('store-top-words','data'))
outputs_topic.append(Output('store-docs-topic','data'))



@app.callback(outputs_topic,[Input('url','search')])

def update_topic_page(topic_id):
    if topic_id == None or topic_id == '':
        raise PreventUpdate
    else:
        title = 'Topic ' + topic_id
        list_words = [view.model.top_words_topic(int(topic_id),nb_words)[w][0] for w in range(nb_words)]
        docs = view.model.documents_for_topic(int(topic_id))
        list_docs = [html.Li(children=view.model.corpus.title(docs[d])+', '+str(view.model.corpus.date(docs[d]))) for d in range(len(docs))]
        list_docs_null = ['' for i in range(len(docs),nb_max_docs)]
        list_display_true = [{'display':'block'} for i in range(len(docs))]
        list_display_false = [{'display':'none'} for i in range(len(docs),nb_max_docs)]
        list_arg = list_words + list_docs + list_docs_null + list_display_true + list_display_false       
        if view.model.corpus.dates==False:
            display= {'display':'none'}
            fig = view.scaled_topics()
        else:
            display = {'display':'block'}
            fig = view.frequency_topic_evolution(int(topic_id))
        list_arg.insert(0,title)

        list_arg.append(display)
        list_arg.append(fig)
        
        list_arg.append(list_words)
        list_arg.append(docs)

    return tuple(list_arg)

inputs_topic = [Input('word'+str(w),'n_clicks') for w in range(nb_words)] +[Input('doc'+str(d),'n_clicks') for d in range(nb_max_docs)]
inputs_topic.insert(0,Input('store-top-words','data'))
inputs_topic.insert(1,Input('store-docs-topic','data'))

@app.callback([Output('store-id-topic-word','data'),Output('store-id-topic-doc','data'),Output('store-path-topic','data')],inputs_topic)
def click_on_words(list_words,list_docs,*args):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if changed_id[0] == 'w':
        return view.model.corpus.id_for_word(list_words[int(changed_id[4:-9])]),'','/word'
    elif changed_id[0] == 'd'  and int(changed_id[3:-9])<len(list_docs):
        return '',str(list_docs[int(changed_id[3:-9])]),'/doc'
    else :
        raise PreventUpdate

