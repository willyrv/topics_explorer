import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from apps import overview, topic, dictionary

from navbar import Navbar

nav = Navbar()


app.layout = html.Div([
    nav,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


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