# from re import I
import time
from dash import Dash, dcc, html, dash_table, State
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime
import os

"""
1. Test file -> df_viewer.loc[:15] <remove the line>
2. dcc.Dropdown(id='dpdn-data-selection', multi=False, value=dir_list[-1], 
    -> need to change multiple selection mode and make function can merge the selected dataframes
3. auto width of data-viewer cells
4. Do I need to set all columns as default when I display data on data viewer?
5. Need to arange functions
6. If we need to run this program as a server, we need to justify the button timestamp for optimal one

"""


global data_path
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


# Default dataframe
df_viewer = pd.read_sas('hn19_all.sas7bdat', encoding='iso-8859-1', format='sas7bdat') ##

df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]
df_viewer = df_viewer.loc[:15] # need to remove
data=[{'col_name':i,'col_type':str(type(df_viewer.iloc[1][i]))} for i in df_viewer.columns]
print(data)
app = DashProxy(__name__, prevent_initial_callbacks=True, transforms=[MultiplexerTransform()],external_stylesheets=[dbc.themes.BOOTSTRAP],
            meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}])

app.layout = dbc.Container([
    dbc.Row([
        # Columns selection
        dbc.Col([
            dash_table.DataTable(
                id='table-col-selection',
                # columns=[{'name': i, 'id':i} for i in df_viewer.columns],
                # data=df_viewer.to_dict('records'),
                columns=[{'name':'col_name','id':'col_name'},{'name':'col_type','id':'col_type'}],
                # df.iloc[i]['BoolCol']
                # data=[{'col_name':i,'col_type':type(df_viewer.iloc[1][i])} for i in df_viewer.columns],
                data=[{'col_name':i,'col_type':str(type(df_viewer.iloc[1][i])).replace("<class '",'').replace("'>",'')} for i in df_viewer.columns],
                virtualization=True,
                row_selectable='multi',
                selected_rows=[],
                fixed_rows={'headers': True},
                style_cell={'minWidth': 70, 'width': 100, 'maxWidth': 140},
                # style_cell={"autoWidth":True}, # need to find some other method for adjust auto width
                style_table={'height': 400},
            )
            ]
        ),
    ]),
]) # , fluid = True



if __name__ == '__main__':
    app.run_server(debug=True)