import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app,view

layout = html.Div([
    html.H3(id='word-id')
])

@app.callback(Output('word-id','children'),[Input('url','search')])

def update_word(word_id):
    if word_id == '':
        raise PreventUpdate
    else :
        return view.model.corpus.word_for_id(int(word_id))