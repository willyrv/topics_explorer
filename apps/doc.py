import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app,view

nb_docs = 10

layout = html.Div([
    dcc.Store(id='store-related-docs',storage_type='session',clear_data=True),
    dbc.Row(dbc.Col(html.Div(['Click to select a document']),width={"size": 6, "offset": 1})),
    html.Br(),
    dbc.Row(dbc.Col(
        dbc.Select(
            id = 'doc-selection',
            options = [{'label': view.model.corpus.title(id),'value' : id} for id in range(view.model.corpus.size)]            
        ),
        width={"size": 6, "offset": 1}       
       
    )),
    dbc.Col([html.Br(),
    html.H3(id='title-doc'),
    html.Br(),
    html.H6(id='date-doc'),
    html.Br(),
    html.Div(id='full-doc')],
    width={"size": 12}),
    html.Br(),
    dbc.Col([
        html.H5("Related documents"),
        html.Ul([html.Div(id = 'related-doc' + str(doc)) for doc in range(nb_docs)]),
    ])
])
inputs_doc = [Input('related-doc'+str(d),'n_clicks') for d in range(nb_docs)]
inputs_doc.insert(0,Input('store-id-topic-doc','data'))
inputs_doc.insert(1,Input('store-related-docs','data'))

@app.callback(Output('doc-selection','value'),inputs_doc)

def update_doc_selection(doc_id,list_related_docs,*args):
    ctx = dash.callback_context
    c = ctx.triggered[0]['prop_id'].split('.')[0]
    if doc_id=='' or c =='store-related-docs':
        raise PreventUpdate
    elif c!='' and  c[0] =='r':
        return str(list_related_docs[int(c[-1])])
    else:
        return doc_id


outputs_doc = [Output('related-doc'+ str(doc),'children') for doc in range(nb_docs)]
outputs_doc.append(Output('title-doc','children'))
outputs_doc.append(Output('date-doc','children'))
outputs_doc.append(Output('full-doc','children'))
outputs_doc.append(Output('store-related-docs','data'))

@app.callback(outputs_doc,[Input('doc-selection','value')])

def update_doc(doc_id):

    if doc_id == None or doc_id == '':
        raise PreventUpdate
    else:
        list_related_docs = view.model.closest_docs(doc_id,nb_docs)
        list_arg = [html.Li(children=view.model.corpus.title(d)+', '+str(view.model.corpus.date(d))) for d in list_related_docs]
        title = 'Document ' + doc_id +': ' + view.model.corpus.title(int(doc_id))
        date = 'published in ' + str(view.model.corpus.date(int(doc_id)))
        full_text = view.model.corpus.full_text(int(doc_id))
        list_arg.append(title)
        list_arg.append(date)
        list_arg.append(full_text)
        list_arg.append(list_related_docs)
        return tuple(list_arg)

