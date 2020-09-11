import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
from dash.exceptions import PreventUpdate
import pandas as pd
import shutil
import os

import dash_table
from app import app

df = pd.read_csv('available_datasets.csv',sep='|')

layout = html.Div([
    dbc.Row(dbc.Col([html.Br(),html.H3("Available datasets"),html.Br(),],width={"size":10}),justify='center'),
    dbc.Row(
        dbc.Col([
            dash_table.DataTable(
                id='table-corpus',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                row_selectable='single',
                row_deletable=True,
                style_cell={'textAlign':'center'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'}
            ),
            dcc.Interval(
                id='interval-component',
                interval=60*1000, 
                n_intervals=0
            ),
            dbc.ButtonGroup([
                dbc.Button("Upload a new dataset",id='add-button',n_clicks=0),
                dbc.Button("Save",id='save-button',n_clicks=0)
            ],
            size='lg'),
            

        ],
        width={"size":8}
        ),
        justify='center'),
        dbc.Row(dbc.Col([
            html.Ul(id="output-1",children=[html.Li("Choose a dataset by selecting a row"),html.Li("Press save to confirm changes such as dataset deletions")]),
            html.Br(),
            html.Br(),
            html.H5(id='selected-dataset')],width={"size":10}),justify='center')
    

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
    if btn==0:
        raise PreventUpdate
    else:
        return '/upload'

@app.callback(
        Output("output-1","children"),
        [Input("save-button","n_clicks")],
        [State("table-corpus","data")]
        )

def selected_data_to_csv(nclicks,table): 
    if nclicks == 0:
        raise PreventUpdate
    else:
        pd.DataFrame(table).to_csv('available_datasets.csv',index=False,sep='|')
        return "Data Submitted"

@app.callback(Output('table-corpus', 'data'),
              [Input('interval-component', 'n_intervals')])
def update_table(n):
    df = pd.read_csv('available_datasets.csv',sep='|')
    for dataset_name in os.listdir("assets"):
        if not(dataset_name=='demo'):
            a = df.loc[(df['name'] == dataset_name.split('_')[0])]
            b = df.loc[(df['number_topics'] == int(dataset_name.split('_')[1][:-6]))]
            if a.empty or b.empty:
                dir_path = 'assets/{}'.format(dataset_name)
                shutil.rmtree(dir_path)
        if os.path.exists('assets/{}/model.pickle'.format(dataset_name)):
            df.loc[df['name']== dataset_name.split('_')[0]].replace({"loading":'uploading'},'ready')
    return df.to_dict('records')
