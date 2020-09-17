import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app, update_view_object

def dictionary_layout(view):

    '''Index of all the words'''

    layout = dbc.Row([
        dbc.Col(
            html.Div([
                html.Br(),
                html.H3("Dictionary"),
                dbc.ListGroup([
                    dbc.ListGroupItem(id='dictionary-word' + str(i),children=list(view.model.corpus.index_words.values())[i]) for i in range(len(view.model.corpus.index_words))
                    ])
                ]),
                width={"size": 10}
            )
    ],
    justify='center')
    return layout

