import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate

from app import app,view,available_topics

nb_words = 50

layout = html.Div(children=[
    dbc.Row(dbc.Col(html.Div([
                html.Br(),
                html.H3(id='title-topic')]),
                width={'offset':1})),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.Br(),
                html.H5("Top words"),
                dbc.ListGroup([dbc.ListGroupItem(id='word'+str(w)) for w in range(nb_words)])
            ]),
            width={"size": 3, "offset": 1}
        ),
        dbc.Col(dcc.Graph(id='frequency-per-years'))
    ])
])

outputs = [Output('word'+str(w),'children') for w in range(nb_words)]
outputs.insert(0,Output('title-topic','children'))
outputs.append(Output('frequency-per-years','figure'))

@app.callback(outputs,[Input('url','search')])

def update_topic_page(topic_id):
    if topic_id == None or topic_id == '':
        raise PreventUpdate
    else:
        title = 'Topic ' + topic_id
        list_words = [view.model.top_words_topic(int(topic_id),nb_words)[w][0] for w in range(nb_words)]
        fig = view.frequency_topic_evolution(int(topic_id))     

    return title,*list_words, fig