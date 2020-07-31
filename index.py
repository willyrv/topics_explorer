import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from app import app,view
from apps import overview, topic, dictionary

from navbar import Navbar

nav = Navbar()


app.layout = html.Div([
    nav,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='store-nb',storage_type='session',clear_data=True),
    dcc.Store(id='store-path',storage_type='session',clear_data=True)
])
inputs = [Input(str(id),'n_clicks') for id in range(view.model.number_topics)]
inputs.insert(0,Input('store-nb','data'))

@app.callback([Output('url','search'),Output('url','pathname')],inputs)

def update_pathname(topic_store,*args):
    ctx = dash.callback_context
    if (not ctx.triggered or ctx.triggered[0]['prop_id'].split('.')[0]=='store-nb') and topic_store==None :
        raise PreventUpdate
    elif  ctx.triggered[0]['prop_id'].split('.')[0]=='store-nb':
        return topic_store,'/topic'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        return str(button_id),'/topic'


@app.callback(Output('page-content', 'children'),[Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return overview.layout
    elif pathname == '/topic':
        return topic.layout
    elif pathname == '/dictionary':
        return dictionary.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)