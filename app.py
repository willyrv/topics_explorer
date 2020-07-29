#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dash
import dash_bootstrap_components as dbc


from model.corpus import Corpus
from model.topic_model import TopicModel
from model.visualisation import Views

arxiv = './input/arxiv_test.csv'
ASRS = './input/ASRS_test.csv'

nb_topics = 10

model = TopicModel(Corpus(source_file_path=ASRS),nb_topics)
view = Views(model)
available_topics = list(range(model.number_topics))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.FLATLY])

server = app.server
