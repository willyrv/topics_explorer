import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate
import copy

from app import app,view,available_topics

nb_words = 50

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
            html.Ul(id='doc-container'),
        ])
    ])
])

outputs_topic = [Output('word'+str(w),'children') for w in range(nb_words)]
outputs_topic.insert(0,Output('title-topic','children'))
outputs_topic.append(Output('graph-frequency-container','style'))
outputs_topic.append(Output('frequency-per-years','figure'))
outputs_topic.append(Output('doc-container','children'))
outputs_topic.append(Output('store-top-words','data'))
outputs_topic.append(Output('store-docs-topic','data'))



@app.callback(outputs_topic,[Input('url','search')])

def update_topic_page(topic_id):
    if topic_id == None or topic_id == '':
        raise PreventUpdate
    else:
        title = 'Topic ' + topic_id
        list_arg = [view.model.top_words_topic(int(topic_id),nb_words)[w][0] for w in range(nb_words)]
        list_words = copy.copy(list_arg)
        list_docs = view.model.documents_for_topic(int(topic_id))
        if view.model.corpus.dates==False:
            display= {'display':'none'}
            fig = view.scaled_topics()
        else:
            display = {'display':'block'}
            fig = view.frequency_topic_evolution(int(topic_id))
        list_arg.insert(0,title)
        list_arg.append(display)
        list_arg.append(fig)
        list_arg.append([html.Li(
            children=view.model.corpus.title(doc)+', '+str(view.model.corpus.date(doc)),
            id = 'doc' + str(doc)
            ) for doc in view.model.documents_for_topic(int(topic_id))])
        list_arg.append(list_words)
        list_arg.append(list_docs)

    return tuple(list_arg)

inputs_topic = [Input('word'+str(w),'n_clicks') for w in range(nb_words)] +[Input('doc'+str(d),'n_clicks') for d in range(2)] # à changer 
inputs_topic.append(Input('store-top-words','data'))
inputs_topic.append(Input('store-docs-topic','data'))

@app.callback([Output('store-id-topic','data'),Output('store-path-topic','data')],inputs_topic)
def click_on_words(list_words,list_docs,*args):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if changed_id == None or changed_id == 'store-top-words.data':
        raise PreventUpdate
    elif changed_id[0] == 'w':
        return view.model.corpus.id_for_word(list_words[int(changed_id[4])]),'/word'
    else :
        return list_docs(int(changed_id[3:])),'./doc'

