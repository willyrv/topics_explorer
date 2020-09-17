#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''This file permits to initialize the dash app.'''
import dash
import dash_bootstrap_components as dbc
import pickle
import os

nb_docs = 10 #:number of displayed documents in the lists in topic,doc and word page
nb_words = 10 #:number of displayed words in the lists in topic,doc and word page

def update_view_object():
    '''Update view object in fonction of user's selection of an available dataset'''
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

