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
    dbc.Row(
        dbc.Col([
            html.Br(),
            html.H3("Available datasets"),
            html.Br(),
            dash_table.DataTable(
                id='table-corpus',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                row_selectable='single',
                row_deletable=True
            ),
            dbc.ButtonGroup([
                dbc.Button("Add",id='add-button',n_clicks=0),
                dbc.Button("Delete",id='delete-button',n_clicks=0)
            ],
            size='lg'),
            html.Br(),
            html.Br(),
            html.H5(id='selected-dataset')

        ],
        width={"size":10}
        ),
        justify='center')
    

])

@app.callback(Output('selected-dataset','children'),[Input('table-corpus','derived_virtual_data'),Input('table-corpus','derived_virtual_selected_rows')])

def update_choice_corpus(rows,selection):
    if selection == None or rows==None or selection == []:
        raise PreventUpdate
    else : 
        file = open('path_model.txt','w')
        file.write('assets/{}_{}topics/'.format(rows[selection[0]]['name'],rows[selection[0]]['number_topics']))
        file.close()
    return 'Selected dataset :' + rows[selection[0]]['name']

@app.callback(Output('store-path-select-corpus','data'),[Input('add-button','n_clicks')])

def update_page_with_add_button(btn):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if not('add-button' in changed_id):
        raise PreventUpdate
    return '/upload'





