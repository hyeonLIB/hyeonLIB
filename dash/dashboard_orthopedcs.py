from pydoc import classname
from turtle import width
from dash import Dash, dcc, html, Output, Input, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime
import os

data_path = './raw_data'
dir_list = os.listdir(data_path)
dir_list.sort()


"""Data load methods"""

def load_data(file_name,data_path, to_csv=False):
    print(file_name)
    file_name = file_name.replace('.sas7bdat','')
    df = pd.read_sas(f'{data_path}/{file_name}.sas7bdat', encoding='iso-8859-1', format='sas7bdat')
    print("data loaded successfully")
    
    if to_csv==True:
        df.to_csv(f'{data_path}/csv/{file_name}.csv', index=False)
        print("data has been saved to csv in csv directory")

    print("*** print 5 rows of data ***\n")
    print(df.head())
    print("*** column list ***\n")
    # print(df.columns.tolist())
    
    return df


df_viewer = pd.read_sas('hn16_all.sas7bdat', encoding='iso-8859-1', format='sas7bdat')

df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]
df_viewer = df_viewer.loc[:15]
df = pd.read_csv("mystocks.csv")
print(df[:15])
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
            meta_tags=[{'name': 'viewport',
                        'content': 'width=device-width, initial-scale=1.0'}]
            )

# Layout section: Bootstrap
# --------------------------------------------------------------

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1("Stock Market dashboard",
                    className='text-center text-primary, mb-4'), # mb-4 -> some padding
            width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='dpdn-data-selection', multi=False, value=dir_list[-1],  # need to change to multiple selection mode
                        options = [{'label':x, 'value':x} for x in dir_list]),  # Done
            # html.H1(""),
            dcc.Checklist(
                id="checklist-data-selection",
                options=[{"label": file_name, "value": file_name} for file_name in dir_list],
                labelStyle={"display": "block"},
                style={"height":300, "width":415, "overflow":"auto"},
                value=[],
            )],
            width = {'size':4}),

        dbc.Col(
            [
            dcc.Dropdown(id='dpdn-col-selection', multi=True, value=['PFE','BNTX'],
                        options=[{'label':column, 'value':column} for column in sorted(df_viewer.columns)]),
            # html.H1(""),
            dcc.Checklist(
                id="checklist-col-selection",
                options=[{"label": column, "value": column} for column in df_viewer.columns],  
                labelStyle={"display": "block"},
                style={"height":300, "width":415, "overflow":"auto"},
                value=[])
            ],
            width = {'size':4}),

        dbc.Col([dcc.Graph(id='line-fig3', figure={})], # need to change
            width = {'size':3})
    ]),
    dbc.Row([ 
        dash_table.DataTable(
            data=df_viewer.to_dict('records'),
            columns=[{'id': i, 'name': i} for i in df_viewer.columns],
            virtualization=True,
            fixed_rows={'headers': True},
            style_cell={'minWidth': 80, 'width': 80, 'maxWidth': 80},
            style_table={'height': 400}  # default is 500
        )
    ])
]) 


if __name__ == '__main__':
    app.run_server(debug=True)