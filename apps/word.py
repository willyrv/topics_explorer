import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app,view

nb_docs = view.model.nb_docs

layout = html.Div([
    dcc.Store(id='store-all-docs-word',storage_type='session',clear_data=True),
    dcc.Store(id='store-docs-word',storage_type='session',clear_data=True),
    dcc.Store(id='nb-page-docs-word',storage_type='session',clear_data=True),
    dcc.Store(id='nb-docs-for-word',storage_type='session',clear_data=True),
    dcc.Store(id='nb-docs-for-word-2',storage_type='session',clear_data=True),
    dbc.Row(
        dbc.Col(html.Div(['Click to select a word']),width={"size": 10}),
        justify='center'),
    html.Br(),
    dbc.Row(
        dbc.Col(
            dbc.Select(
                id = 'word-selection',
                options = [{'label': id,'value' : w} for w,id in view.model.corpus.index_words.items()],
                value='1'
            ),
            width={"size": 10}
        ),
        justify='center'
        ),
    dbc.Row(
        dbc.Col([
            html.Br(),
            html.H3(id='word-id'),
            html.Div(id = 'stats-word'),
            html.Br(),
            html.Br()
        ],width={"size":10}),
        justify='center'),
    dbc.Row([
        dbc.Col([
            html.H5(id='title-docs-word'),
            html.Br(),
            html.Ul([html.Div(id = 'docs-word' + str(doc)) for doc in range(nb_docs)]),
            dbc.Button('Previous',id='previous-docs-word',n_clicks=0),
            dbc.Button('Next',id='next-docs-word',n_clicks=0),
            html.Div(id='display-nb-docs-word')
            ],
            width={"size": 5}),
        dbc.Col([
            html.H5('Proportion of time the word is assigned to each topic'),
            dcc.Graph(id= 'freq-word'),
            html.H6('Click on a bar to have more informations about a topic')
            ],
            width={"size": 5}),
        ],
        justify='center')  
])

@app.callback(Output('word-selection','value'),[Input('store-id-topic-word','data')])

def initialisation_word(word_id):
    if word_id == '' or word_id == None:
        return '1'
    else :
        return word_id

@app.callback([
    Output('word-id','children'),
    Output('stats-word','children'),
    Output('freq-word','figure'),
    Output('title-docs-word','children'),
    Output('nb-docs-for-word','data'),
    Output('nb-docs-for-word-2','data'),
    Output('store-all-docs-word','data'),
    Output('previous-docs-word','n_clicks'),
    Output('next-docs-word','n_clicks')],
    [Input('word-selection','value')])

def update_word(word_id):
    if word_id == '':
        raise PreventUpdate
    else:
        word = view.model.corpus.word_for_id(int(word_id))
        nb_docs_for_word = view.model.nb_docs_for_word(int(word_id))
        figure = view.frequency_word_topics(int(word_id))
        stats_word = 'Number of documents where ' + word + ' is present : ' + str(nb_docs_for_word)
        title_docs_word = 'Documents where ' + word + ' is present '
        list_docs_word = [d for (d,weight) in view.model.docs_for_word(int(word_id))]

        return word,stats_word,figure,title_docs_word,nb_docs_for_word,nb_docs_for_word,list_docs_word,0,0

outputs_word = [Output('docs-word'+ str(doc),'children') for doc in range(nb_docs)]
outputs_word.append(Output('store-docs-word','data'))

@app.callback(outputs_word,[Input('nb-page-docs-word','data'),Input('store-all-docs-word','data'),Input('nb-docs-for-word','data')])

def update_list_doc(id_page,list_docs_word,nb_docs_for_word):
    if id_page == None:
        raise PreventUpdate
    ind = id_page*(nb_docs-1)+id_page
    if ind+nb_docs < nb_docs_for_word:
        list_docs = list_docs_word[ind:ind+nb_docs]
    else:
        list_docs = list_docs_word[ind:nb_docs_for_word] 
    list_arg = [html.Li(children=view.model.corpus.title(d)+', '+str(view.model.corpus.date(d)),style={"cursor":'pointer'}) for d in list_docs] + ['' for i in range(ind+nb_docs-nb_docs_for_word)]
    list_arg.append(list_docs + ['' for i in range(ind+nb_docs-nb_docs_for_word)])
    return tuple(list_arg)

@app.callback([
    Output('display-nb-docs-word','children'),
    Output('nb-page-docs-word','data')],
    [Input('next-docs-word','n_clicks'),
    Input('previous-docs-word','n_clicks'),
    Input('nb-docs-for-word-2','data')])

def update_nb_page_docs_word(btn_next,btn_prev,nb_docs_for_word):
    nb_page = btn_next-btn_prev
    if nb_page < 0 or ((nb_page-1)*nb_docs+1) > (nb_docs_for_word - (nb_docs-1)):
        raise PreventUpdate
    else:
        if nb_docs_for_word < (1 + nb_page)*nb_docs:
            return 'Documents ' + str((nb_page*nb_docs+1)) + ' to ' + str(nb_docs_for_word) + ' of ' + str(nb_docs_for_word),nb_page
        else : 
            return 'Documents ' + str((nb_page*nb_docs+1)) + ' to ' + str((1 + nb_page)*nb_docs) + ' of ' + str(nb_docs_for_word),nb_page

inputs_word = [Input('docs-word'+ str(doc),'n_clicks') for doc in range(nb_docs)]
inputs_word.insert(0,Input('freq-word','clickData'))
inputs_word.insert(1,Input('store-docs-word','data'))

@app.callback([Output('store-id-word','data'),Output('store-path-word', 'data')],inputs_word)

def store_pathname(clickData,list_docs_word,*args):
    ctx = dash.callback_context
    c = ctx.triggered[0]['prop_id'].split('.')[0]
    if c =='store-docs-word' or (c[0]!='d' and clickData == None):
        raise PreventUpdate
    elif c!='' and  c[0] =='d':
        return str(list_docs_word[int(c[-1])]),'/doc'
    else:
        return str(clickData['points'][0]['pointNumber']),'/topic'


