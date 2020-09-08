import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate
import copy

from app import app,update_view_object

view, path = update_view_object()

nb_words = view.model.nb_words
nb_docs = view.model.nb_docs

layout = html.Div(children=[
    dcc.Store(id='store-all-top-words',storage_type='session',clear_data=True),
    dcc.Store(id='store-top-words',storage_type='session',clear_data=True),
    dcc.Store(id='nb-page-top-words',storage_type='session',clear_data=True),
    dcc.Store(id='store-all-docs-topic',storage_type='session',clear_data=True),
    dcc.Store(id='store-docs-topic',storage_type='session',clear_data=True),
    dcc.Store(id='nb-page-docs-topic',storage_type='session',clear_data=True),

    dbc.Row(dbc.Col([
                html.Br(),
                html.H3(id='title-topic')],
                width={'size':10}),
                justify='center'),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H5('Topic frequency evolution'),
            html.Br(),
            html.Div(id='graph-frequency-container',children=[dcc.Graph(id='frequency-per-years')])            
        ],
        width={"size":7}),
        dbc.Col([
            html.H5("Top words"),
            dbc.ListGroup([dbc.ListGroupItem(id='word'+str(w)) for w in range(nb_words)],style={"cursor":'pointer'}),
            dbc.Button('Previous',id='previous-top-words',n_clicks=0),
            dbc.Button('Next',id='next-top-words',n_clicks=0),
            html.Div(id='display-nb-page-words')
        ],
        width={"size":3})
        
    ],
    justify='center'),
    dbc.Row([        
         dbc.Col([
            html.H5('Related documents'),
            html.Ul([html.Li(id = 'doc' + str(doc)) for doc in range(nb_docs)],style={"cursor":'pointer'}),
            dbc.Button('Previous',id='previous-docs-topic',n_clicks=0),
            dbc.Button('Next',id='next-docs-topic',n_clicks=0),
            html.Div(id='display-nb-page-topic')
        ],
        width={"size":6}),
        dbc.Col(            
            html.Div([
                html.Br(),
                html.Br(),
                html.Br(),
                html.Img(id='wordcloud-topic',style={"width": '100%'}),
                               
            ]),
            width={"size": 4}
        )

    ],justify='center')
])

@app.callback([
    Output('title-topic','children'),
    Output('graph-frequency-container','style'),
    Output('frequency-per-years','figure'),
    Output('store-all-top-words','data'),
    Output('previous-top-words','n_clicks'),
    Output('next-top-words','n_clicks'),
    Output('store-all-docs-topic','data'),
    Output('previous-docs-topic','n_clicks'),
    Output('next-docs-topic','n_clicks'),
    Output('wordcloud-topic','src')],
    [Input('url','search')])

def update_topic_page(topic_id):
    if topic_id == None or topic_id == '':
        topic_id = '0'
    title = 'Topic ' + topic_id
    list_words = [w for (w,weight) in view.model.top_words_all_topics[int(topic_id)]]
    docs = [id for (id, weigth) in view.model.top_docs_all_topics[int(topic_id)]]
    if view.model.corpus.dates==False:
        display= {'display':'none'}
        fig = view.scaled_topics()
    else:
        display = {'display':'block'}
        fig = view.frequency_topic_evolution(int(topic_id))
        source = app.get_asset_url(path[7:]+'topic{}.png'.format(topic_id))

    return title,display,fig,list_words,0,0,docs,0,0,source

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

outputs_topic2 = [Output('doc'+str(doc),'children') for doc in range(nb_docs)] + [Output('word'+str(w),'children') for w in range(nb_words)]
outputs_topic2.append(Output('store-docs-topic','data'))
outputs_topic2.append(Output('store-top-words','data'))

@app.callback(outputs_topic2,[Input('nb-page-docs-topic','data'),Input('nb-page-top-words','data'),Input('store-all-docs-topic','data'),Input('store-all-top-words','data')])

def update_lists_topic(id_page_doc,id_page_word,list_docs_topic,list_top_words):
    if id_page_doc == None or id_page_word ==  None:
        raise PreventUpdate
    ind_doc= id_page_doc*(nb_docs-1)+id_page_doc
    list_docs = list_docs_topic[ind_doc:ind_doc+nb_docs]
    ind_word = id_page_word*(nb_words-1)+id_page_word
    list_words =list_top_words[ind_word:ind_word+nb_words]
    list_arg = [view.model.corpus.title(d)+', '+str(view.model.corpus.date(d)) for d in list_docs] + list_words
    list_arg.append(list_docs)
    list_arg.append(list_words)
    return tuple(list_arg)

@app.callback([
    Output('display-nb-page-topic','children'),
    Output('nb-page-docs-topic','data'),
    Output('display-nb-page-words','children'),
    Output('nb-page-top-words','data')],
    [Input('next-docs-topic','n_clicks'),Input('previous-docs-topic','n_clicks'),Input('next-top-words','n_clicks'),Input('previous-top-words','n_clicks')])

def update_nb_page_list_topic(btn_next_doc,btn_prev_doc,btn_next_word,btn_prev_word):
    if btn_next_doc-btn_prev_doc < 0 or btn_next_word-btn_prev_word < 0:
        raise PreventUpdate
    display_doc = 'Documents ' + str((btn_next_doc-btn_prev_doc)*nb_docs+1) + ' to ' + str((1+btn_next_doc-btn_prev_doc)*nb_docs)
    display_word = 'Words ' + str((btn_next_word-btn_prev_word)*nb_words+1) + ' to ' + str((1+btn_next_word-btn_prev_word)*nb_words)
    return display_doc, btn_next_doc-btn_prev_doc, display_word, btn_next_word-btn_prev_word