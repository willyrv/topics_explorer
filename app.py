#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dash
import dash_bootstrap_components as dbc
import pickle


file = open("path_model.txt",'r')
path = file.readlines()[0]
file.close()

f = open(path + 'model.pickle','rb')
view = pickle.load(f)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.LUX])

server = app.server

