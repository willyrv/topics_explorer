import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app,view

nb_docs = 10

layout = html.Div([
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
    width={"size": 10}),
    html.Br(),
    dbc.Col([
        html.H5("Related documents"),
        html.Ul([html.Div(id = 'related-doc' + str(doc)) for doc in range(nb_docs)]),
    ])
])
inputs_doc = [Input('related-doc'+str(d),'n_clicks') for d in range(nb_docs)]
inputs_doc.insert(0,Input('store-id-topic-doc','data'))

@app.callback(Output('doc-selection','value'),inputs_doc)

def update_doc_selection(doc_id,*args):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]    
    if changed_id[0] == 'r':
        return changed_id[11:-9]
    elif changed_id[0] == 's' and doc_id != None :
        return doc_id
    else :
        raise PreventUpdate

outputs_doc = [Output('related-doc'+ str(doc),'children') for doc in range(nb_docs)]
outputs_doc.append(Output('title-doc','children'))
outputs_doc.append(Output('date-doc','children'))
outputs_doc.append(Output('full-doc','children'))

@app.callback(outputs_doc,[Input('doc-selection','value')])

def update_doc(doc_id):

    if doc_id == None :
        raise PreventUpdate
    else:
        list_arg = [html.Li(children=view.model.corpus.title(d)+', '+str(view.model.corpus.date(d))) for d in view.model.closest_docs(doc_id,nb_docs)]
        title = 'Document ' + doc_id +': ' + view.model.corpus.title(int(doc_id))
        date = 'published in ' + str(view.model.corpus.date(int(doc_id)))
        full_text = view.model.corpus.full_text(int(doc_id))
        list_arg.append(title)
        list_arg.append(date)
        list_arg.append(full_text)
        return tuple(list_arg)

