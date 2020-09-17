import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app, update_view_object,nb_docs

def doc_layout(view):
    layout = html.Div([
        dcc.Store(id='store-all-related-docs',storage_type='session',clear_data=True),
        dcc.Store(id='store-related-docs',storage_type='session',clear_data=True),
        dcc.Store(id='nb-page-list-related-docs',storage_type='session',clear_data=True),

        dbc.Row(
            dbc.Col(html.Div(['Click to select a document']),width={"size": 10}),
            justify='center'
            ),
        html.Br(),
        dbc.Row([
            dbc.Col(
                dbc.Select(
                    id = 'doc-selection',
                    options = [{'label': view.model.corpus.title(id),'value' : id} for id in range(view.model.corpus.size)]      
                    ),
                width={"size": 10}       
            )
        ],
        justify='center'),
        dbc.Row(
            dbc.Col([
                html.Br(),
                html.H3(id='title-doc'),
                html.Br(),
                html.H6(id='date-doc'),
                html.Br(),
                html.Div(id='full-doc')],
                width={"size": 10}
            ),
            justify='center'     
        ),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.H5("Related documents"),
                html.Br(),
                html.Ul([html.Div(id = 'related-doc' + str(doc)) for doc in range(nb_docs)],style={"cursor":'pointer'}),
                dbc.Button('Previous',id='previous-related-docs',n_clicks=0),
                dbc.Button('Next',id='next-related-docs',n_clicks=0),
                html.Div(id='display-nb-page-doc')
            ],
            width={"size":5}),
            dbc.Col([
                html.Br(),
                html.H5("Proportion of each topic in the document"),
                dcc.Graph(id='freq-doc'),
                html.H6('Click on a bar to have more informations about a topic')

                ],            
                width={"size" : 5}
            )
            ],
            justify='center'
        )   
        
    ])
    return layout

inputs_doc = [Input('related-doc'+str(d),'n_clicks') for d in range(nb_docs)]
inputs_doc.insert(0,Input('store-id-topic-doc','data'))
inputs_doc.insert(1,Input('store-id-doc-word','data'))
inputs_doc.insert(2,Input('store-related-docs','data'))
inputs_doc.insert(3,Input('previous-view','data'))

@app.callback(Output('doc-selection','value'),inputs_doc)

def update_doc_selection(doc_id_topic,doc_id_word,list_related_docs,prev_view,*args):

    '''Method in a callback which permits to pass on the doc id after a click event triggered by the user on topic,document or word page.'''

    ctx = dash.callback_context
    c = ctx.triggered[0]['prop_id'].split('.')[0]
    if (prev_view=='topic' and doc_id_topic=='') or (prev_view=='word' and doc_id_word=='') or c =='store-related-docs':
        raise PreventUpdate
    elif c!='' and  c[0] =='r':
        return str(list_related_docs[int(c[-1])])
    elif prev_view=='word':
        return doc_id_word
    else:
        return doc_id_topic

@app.callback([
    Output('title-doc','children'),
    Output('date-doc','children'),
    Output('full-doc','children'),
    Output('store-all-related-docs','data'),
    Output('previous-related-docs','n_clicks'),
    Output('next-related-docs','n_clicks'),
    Output('freq-doc','figure')],
    [Input('doc-selection','value')])

def update_doc_page(doc_id):

    '''Method in a callback whose goal is to display the informations corresponding to the selected document.'''

    view = update_view_object()[0]

    if doc_id == None or doc_id == '':
        doc_id='0'
    list_related_docs = view.model.closest_docs(doc_id)        
    title = 'Document ' + doc_id +': ' + view.model.corpus.title(int(doc_id))
    date = 'published in ' + str(view.model.corpus.date(int(doc_id)))
    full_text = view.model.corpus.full_text(int(doc_id))
    fig = view.frequency_doc_topics(int(doc_id))
    return title,date,full_text,list_related_docs,0,0,fig

outputs_doc = [Output('related-doc'+ str(doc),'children') for doc in range(nb_docs)]
outputs_doc.append(Output('store-related-docs','data'))

@app.callback(outputs_doc,[Input('nb-page-list-related-docs','data'),Input('store-all-related-docs','data')])

def update_list_doc(id_page,list_related_docs):

    '''Method in a callback which updates the list of related documents to the selected document.'''

    view = update_view_object()[0]
    if id_page == None:
        raise PreventUpdate
    ind = id_page*9+id_page
    list_docs = list_related_docs[ind:ind+nb_docs]
    list_arg = [html.Li(children=view.model.corpus.title(d)+', '+str(view.model.corpus.date(d))) for d in list_docs]
    list_arg.append(list_docs)
    return tuple(list_arg)

@app.callback([Output('display-nb-page-doc','children'),Output('nb-page-list-related-docs','data')],[Input('next-related-docs','n_clicks'),Input('previous-related-docs','n_clicks')])

def update_nb_page_list(btn_next,btn_prev):

    '''Method in a callback which permits to display the next related documents after a click on the next or the previous button.'''
    
    view = update_view_object()[0]
    nb_page = btn_next - btn_prev
    if nb_page < 0:
        raise PreventUpdate
    return 'Documents ' + str((nb_page)*nb_docs+1) + ' to ' + str((1+nb_page)*nb_docs) + ' of ' + str(view.model.corpus.size), nb_page

@app.callback([Output('store-id-doc','data'),Output('store-path-doc', 'data')],[Input('freq-doc','clickData')])

def store_pathname(clickData):

    '''Method in a callback whose goal is to store the informations after a click event triggered by the user'''

    if clickData == None:
        raise PreventUpdate
    else:
        return str(clickData['points'][0]['pointNumber']),'/topic'
