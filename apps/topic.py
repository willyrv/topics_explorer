import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app,view,available_topics

layout = html.Div(children=[
    html.H3(id='nb_topic'),
    html.Div(
            dcc.Graph(id='dates'))
    
])

@app.callback([Output('nb_topic','children'),Output('dates','figure')],[Input('url','search')])

def update_nb_topic(topic_id):
    if topic_id == None or topic_id == '':
        raise PreventUpdate
    else:
        title="Topic " + topic_id
        return title,view.frequency_topic_evolution(int(topic_id))
 