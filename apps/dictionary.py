import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app,view

layout = html.Div([
    html.H3("Dictionary"),
    html.Ul(
        [html.Li(list(view.model.corpus.index_words.values())[i]) for i in range(len(view.model.corpus.index_words))]
        )
    
])