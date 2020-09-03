import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from dash.exceptions import PreventUpdate
import pandas as pd

import dash_table
from app import app

df = pd.read_csv('available_datasets.csv',sep='|')

layout = html.Div([
    html.H3("Available datasets"),
    dash_table.DataTable(
        id='table-corpus',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        row_selectable='single'
    ),
    html.Div(id='selected-dataset')

])

@app.callback(Output('selected-dataset','children'),[Input('table-corpus','derived_virtual_data'),Input('table-corpus','derived_virtual_selected_rows')])

def update_choice_corpus(rows,selection):
    if selection == None or rows==None or selection == []:
        raise PreventUpdate
    else : 
        file = open('path_model.txt','w')
        file.write('assets/{}_{}topics/'.format(rows[selection[0]]['name'],rows[selection[0]]['number_topics']))
        file.close()
    return 'Selected dataset :' + name