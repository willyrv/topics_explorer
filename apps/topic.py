import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app,view,available_topics

layout = html.Div(children=[
    dcc.Link(
        html.Button("overview"),
        href='/'),
     dcc.Link(
        html.Button("topic"),
        href='/topic'),
    html.H3('Evolution of topic frequency'),
    html.Div(children='''
             Choose a topic
             '''),
            dcc.Graph(
                id='dates')
    
])
@app.callback(Output('dates','figure'),[Input('url','search')])

def update_graph(topic_id):
    if topic_id == None:
        raise PreventUpdate
    else:
        return view.frequency_topic_evolution(int(topic_id))
 