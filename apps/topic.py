import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate
import copy

from app import app,view

nb_words = view.model.nb_words
nb_docs = view.model.nb_docs

layout = html.Div(children=[
    dcc.Store(id='store-top-words',storage_type='session',clear_data=True),
    dcc.Store(id='store-all-docs-topic',storage_type='session',clear_data=True),
    dcc.Store(id='store-docs-topic',storage_type='session',clear_data=True),
    dcc.Store(id='nb-page-docs-topic',storage_type='session',clear_data=True),

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
            html.Ul([html.Div(id = 'doc' + str(doc)) for doc in range(nb_docs)]),
            dbc.Button('Previous',id='previous-docs-topic',n_clicks=0),
            dbc.Button('Next',id='next-docs-topic',n_clicks=0),
            html.Div(id='display-nb-page-topic')
        ])
    ])
])

outputs_topic = [Output('word'+str(w),'children') for w in range(nb_words)]
outputs_topic.insert(0,Output('title-topic','children'))
outputs_topic.append(Output('graph-frequency-container','style'))
outputs_topic.append(Output('frequency-per-years','figure'))
outputs_topic.append(Output('store-top-words','data'))
outputs_topic.append(Output('store-all-docs-topic','data'))
outputs_topic.append(Output('previous-docs-topic','n_clicks'))
outputs_topic.append(Output('next-docs-topic','n_clicks'))



@app.callback(outputs_topic,[Input('url','search')])

def update_topic_page(topic_id):
    if topic_id == None or topic_id == '':
        raise PreventUpdate
    else:
        title = 'Topic ' + topic_id
        list_words = [view.model.top_words_all_topics[int(topic_id)][w][0] for w in range(nb_words)]
        docs = [id for (id, weigth) in view.model.top_docs_all_topics[int(topic_id)]]
        list_arg = list_words   
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
        list_arg.append(0)
        list_arg.append(0)

    return tuple(list_arg)

inputs_topic = [Input('word'+str(w),'n_clicks') for w in range(nb_words)] +[Input('doc'+str(d),'n_clicks') for d in range(nb_docs)]
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

outputs_topic2 = [Output('doc'+str(doc),'children') for doc in range(nb_docs)]
outputs_topic2.append(Output('store-docs-topic','data'))

@app.callback(outputs_topic2,[Input('nb-page-docs-topic','data'),Input('store-all-docs-topic','data')])

def update_list_doc_topic(id_page,list_docs_topic):
    if id_page == None:
        raise PreventUpdate
    ind = id_page*9+id_page
    list_docs = list_docs_topic[ind:ind+nb_docs]
    list_arg = [html.Li(children=view.model.corpus.title(d)+', '+str(view.model.corpus.date(d))) for d in list_docs]
    list_arg.append(list_docs)
    return tuple(list_arg)

@app.callback([Output('display-nb-page-topic','children'),Output('nb-page-docs-topic','data')],[Input('next-docs-topic','n_clicks'),Input('previous-docs-topic','n_clicks')])

def update_nb_page_list_topic(btn_next,btn_prev):
    if btn_next-btn_prev < 0:
        raise PreventUpdate
    return 'Documents ' + str((btn_next-btn_prev)*10+1) + ' to ' + str((1+btn_next-btn_prev)*10), btn_next-btn_prev