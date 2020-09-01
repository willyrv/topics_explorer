import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash_table

import pandas as pd

from model.corpus import Corpus
from model.topic_model import TopicModel
from model.visualisation import Views
from wordcloud import WordCloud

import pickle

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H3('Upload your dataset'),
    html.H5('Informations'),
    dbc.InputGroup(
        [
            dbc.InputGroupAddon("Dataset's name", addon_type="prepend"),
            dbc.Input()            
        ],
        className="mb-3",
        id='dataset-name'
    ),
    dbc.InputGroup(
        [
            dbc.InputGroupAddon("Description", addon_type="prepend"),
            dbc.Textarea()            
        ],
        className="mb-3",
        id='dataset-description'
    ),
    dbc.InputGroup(
        [
            dbc.InputGroupAddon("Number of topics", addon_type="prepend"),
            dbc.Input(type="number")            
        ],
        className="mb-3",
        id='choice-nb-topics'
    ),
    html.H5('File'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        multiple=False
    ),
    html.Div(id='output-data-upload'),
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')),sep='|')
    except Exception as e:
        print(e)
        return html.Div([
        'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

def build_model(name,contents,filename,date,nb_topics,nb_words=10,nb_docs=10):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')),sep='|')
    except Exception as e:
        print(e)
        return html.Div([
        'There was an error processing this file.'
        ])
    print(nb_topics)

    model = TopicModel(Corpus(df),nb_topics,nb_words,nb_docs)
    view = Views(model)

    f = open('assets/{}_{}topics.pickle'.format(name,nb_topics),'wb')
    pickle.dump(view,f)
    f.close()

    complete_corpus = ','.join(view.model.corpus.data['text'])
    wc = WordCloud(background_color="white", max_words=1000, contour_width=3, contour_color="steel blue")
    cloud = wc.generate(complete_corpus)
    cloud.to_file('assets/{}_corpus.png'.format(name))

    for i in range(view.model.number_topics):
        freq_words = view.model.topic_word_matrix[0,:]
        d = {view.model.corpus.word_for_id(id): freq_words[id] for id in range(len(view.model.corpus.index_words))} 
        cloud_top = wc.generate_from_frequencies(d)
        cloud_top.to_file('assets/{}_topic{}.png'.format(name,i))


@app.callback(Output('output-data-upload', 'children'),
              [Input('dataset-name','children'),Input('choice-nb-topics','children'),Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(input_name,choice_nb_topics,content, filename, date):
    if content is not None:
        name = input_name[1]['props']['value']
        nb_topics = choice_nb_topics[1]['props']['value']
        build_model(name,content,filename,date,nb_topics)
        children = 'ça a marché youpi'
            
        return children



if __name__ == '__main__':
    app.run_server(debug=True)