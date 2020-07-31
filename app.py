#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dash
import dash_bootstrap_components as dbc
import pickle

f = open('views_model.pickle','rb')
view = pickle.load(f)

available_topics = list(range(view.model.number_topics))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.FLATLY])

server = app.server

