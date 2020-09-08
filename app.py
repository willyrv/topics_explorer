#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dash
import dash_bootstrap_components as dbc
import pickle
import os

def update_view_object():
    file = open("path_model.txt",'r')
    path = file.readlines()[0]
    file.close()
    if not(os.path.exists(path + 'model.pickle')):
        path ='assets/demo/'

    f = open(path + 'model.pickle','rb')
    view = pickle.load(f)
    return view, path

app = dash.Dash(__name__,suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.LUX],title='Topics explorer')

server = app.server

