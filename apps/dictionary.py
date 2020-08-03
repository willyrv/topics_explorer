import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app,view

layout = dbc.Row([
    dbc.Col(
        html.Div([
            html.Br(),
            html.H3("Dictionary"),
            dbc.ListGroup([
                dbc.ListGroupItem(list(view.model.corpus.index_words.values())[i]) for i in range(len(view.model.corpus.index_words))
                ])
            ]),
            width={"size": 8, "offset": 1}
        )
])

