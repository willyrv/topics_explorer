import base64
import datetime
import io
import os

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash_table

import pandas as pd
import csv

from model.corpus import Corpus
from model.topic_model import TopicModel
from model.visualisation import Views
from wordcloud import WordCloud
from app import app

import pickle

layout = html.Div([
    dbc.Row(dbc.Col([
        html.Br(),
        html.H3('Upload your dataset'),
        html.Br(),
        html.Br(),
        html.H5('Informations'),
        html.Br(),
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
                dbc.InputGroupAddon("Number of documents", addon_type="prepend"),
                dbc.Input(type="number")            
            ],
            className="mb-3",
            id='size-corpus'
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Number of topics", addon_type="prepend"),
                dbc.Input(type="number")            
            ],
            className="mb-3",
            id='choice-nb-topics'
        ),
        html.Br(),
        html.H5('File'),
        html.Br(),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                html.A('Click to select a file')
            ]),
            multiple=False
        ),
        html.Div(id='output-data-upload'),

    ],width={"size":10}),justify='center')
    
])
def build_model(name,contents,filename,date,nb_topics,nb_words=10,nb_docs=10):
    content_string = contents.split(',')[1]

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

    model = TopicModel(Corpus(df),nb_topics,nb_words,nb_docs)
    view = Views(model)

    path = 'assets/{}_{}topics/'.format(name,nb_topics)
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)


    f = open(path + 'model.pickle','wb')
    pickle.dump(view,f)
    f.close()

    complete_corpus = ','.join(view.model.corpus.data['text'])
    wc = WordCloud(width = 1024,height=512,background_color="white", max_words=1000, contour_width=3, contour_color="steel blue")
    cloud = wc.generate(complete_corpus)
    cloud.to_file(path + 'corpus.png')

    for i in range(view.model.number_topics):
        freq_words = view.model.topic_word_matrix[i,:]
        d = {view.model.corpus.word_for_id(id): freq_words[id] for id in range(len(view.model.corpus.index_words))} 
        cloud_top = wc.generate_from_frequencies(d)
        cloud_top.to_file(path + 'topic{}.png'.format(i))

    return path


@app.callback(Output('output-data-upload', 'children'),
              [Input('dataset-name','children'),Input('dataset-description','children'),Input('choice-nb-topics','children'),Input('size-corpus','children'),Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_csv(input_name,input_description,choice_nb_topics,input_size,content, filename, date):
    if not(os.path.exists('available_datasets.csv')):
        header = ['name', 'description', 'size','number_topics','loading']
        with open('available_datasets.csv', 'wt', newline ='') as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerow(i for i in header)
        file.close()

    if content is not None:
        name = input_name[1]['props']['value']
        description = input_description [1]['props']['value']
        nb_topics = choice_nb_topics[1]['props']['value']
        size = input_size[1]['props']['value']
        myCsvRow = [name,description,str(size),str(nb_topics),'ready']

        with open('available_datasets.csv','a',newline='') as f:
            writer = csv.writer(f,delimiter='|')
            writer.writerow(myCsvRow)
            f.close()
        
        children = build_model(name,content,filename,date,nb_topics)
            
        return children