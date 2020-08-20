import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app,view

layout = html.Div([
    dbc.Row(dbc.Col(html.Div(['Click to select a word']),width={"size": 3, "offset": 1})),
    html.Br(),
    dbc.Row(dbc.Col(
        dbc.Select(
            id = 'word-selection',
            options = [{'label': id,'value' : w} for w,id in view.model.corpus.index_words.items()]
        ),
        width={"size": 3, "offset": 1}
    )),
    html.Br(),
    html.H3(id='word-id'),
    html.Div(id = 'stats-word')

])

@app.callback(Output('word-selection','value'),[Input('store-id-topic-word','data')])

def initialisation_word(word_id):
    if word_id == '' or word_id == None:
        raise PreventUpdate
    else :
        return word_id

@app.callback([Output('word-id','children'),Output('stats-word','children')],[Input('word-selection','value')])

def update_word(word_id):
    if word_id == '':
        raise PreventUpdate
    else:
        word = view.model.corpus.word_for_id(int(word_id))
        nb_docs = view.model.nb_docs_for_word(int(word_id))

        return word,'Documents where ' + word + ' is present : ' + str(nb_docs)
