import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app,view

layout = html.Div([
    html.H3(id='doc-id')
])

@app.callback(Output('doc-id','children'),[Input('url','hash')])

def update_doc(doc_id):
    return 'Document ' + doc_id