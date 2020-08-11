import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app,view

layout = html.Div([
    dbc.Select(
        id = 'word-selection',
        options = [{'label': id,'value' : w} for w,id in view.model.corpus.index_words.items()]
    ),
    html.H3(id='word-id')

])

@app.callback(Output('word-selection','value'),[Input('store-id-topic','data')])

def initialisation_word(word_id):
    if word_id == '':
        raise PreventUpdate
    else :
        return word_id

@app.callback(Output('word-id','children'),[Input('word-selection','value')])

def update_word(word):
    if word == '':
        raise PreventUpdate
    else:
        return view.model.corpus.word_for_id(int(word))
