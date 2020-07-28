import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output

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
             html.Div([
                 dcc.Dropdown(
                     id='topic-id',
                     options=[{'label':"Topic " + str(i),'value':i} for i in available_topics])
                     
             ]),
            dcc.Graph(
                id='dates')
    
])
@app.callback(Output('dates','figure'),[Input('topic-id','value'),Input('url','search')])

def update_graph(topic_id,topic_init):
    if topic_id == None:
        return view.frequency_topic_evolution(int(topic_init))
    else:
        return view.frequency_topic_evolution(topic_id)