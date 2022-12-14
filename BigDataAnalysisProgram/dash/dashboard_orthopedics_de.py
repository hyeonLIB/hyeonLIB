# from re import I
import time
# from dash import Dash, dcc, html, Output, Input, dash_table, State
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform
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

# Application
# -------------------------------------------------------------
app = DashProxy(__name__, prevent_initial_callbacks=True, transforms=[MultiplexerTransform()],external_stylesheets=[dbc.themes.BOOTSTRAP],
            meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}])

# Layout section: Bootstrap
# --------------------------------------------------------------

app.layout = dbc.Container([
    # Title of the application
    dbc.Row([
        dbc.Col(
            html.H1("???????????????????????? ?????? ????????????",
                    className='text-center text-primary, mb-4',
                    style = {"margin-top":"10px"}), # mb-4 -> some padding
            width=12)
    ]),

    dbc.Row([
        # Data selection
        dbc.Col([
            dcc.Dropdown(id='dpdn-data-selection', multi=False, value=dir_list[-1],  # need to change to multiple selection mode
                        options = [{'label':x, 'value':x} for x in dir_list],
                        style = {"margin-bottom":"18px"}),
            dcc.Checklist(
                id="checklist-data-selection",
                options=[{"label": file_name, "value": file_name} for file_name in dir_list],
                labelStyle={"display": "block"},
                style={"height":300, "width":415, "overflow":"auto", "fontSize":18},
                labelClassName='pb-3',
                value=[''])
            # dcc.RadioItems( # need to change to checklist that can offer dataframe merge
            #     id="radiobtn-data-selection",
            #     options=[{"label": file_name, "value": file_name} for file_name in dir_list],
            #     labelStyle={"display": "block"},
            #     style={"height":300, "width":415, "overflow":"auto", "fontSize":18},
            #     labelClassName='pb-3',
            #     value=[]
            # )
            ], width = {'size':4}
        ),
        
        # Columns selection
        dbc.Col([
            dcc.Dropdown(id='dpdn-col-selection', multi=True, value=[], # default select all?
                        options=[{'label':column, 'value':column} for column in sorted(df_viewer.columns)],  # % sorted ?
                        style = {"margin-bottom":"18px"}),
            dcc.Checklist(
                id="checklist-col-selection",
                options=[{"label": column, "value": column} for column in df_viewer.columns],  
                labelStyle={"display": "block"},
                style={"height":300, "width":415, "overflow":"auto", "fontSize":18, "margin-bottom":"18px"},
                labelClassName='pb-1',
                value=[]),
            html.Button(id='btn-col-all', n_clicks=0, children="Select all", style={"margin-right":"250px"}),
            html.Button(id='btn-col-update', n_clicks=0, n_clicks_timestamp=0, children="Update")  ## you should place to the right side
            ], width = {'size':4}
        ),

        # Properties of columns
        dbc.Col([dcc.Graph(id='line-fig3', figure={})], ## need to change
            width = {'size':3}
        )
    ]),

    # Data viewer
    dbc.Row([ 
        dash_table.DataTable(
            id='data-viewer',
            data=df_viewer.to_dict('records'),
            columns=[{'id': i, 'name': i} for i in df_viewer.columns],
            virtualization=True,
            fixed_rows={'headers': True},
            style_cell={'minWidth': 70, 'width': 100, 'maxWidth': 140},
            # style_cell={"autoWidth":True}, # need to find some other method for adjust auto width
            style_table={'height': 400},
        )
    ])
]) # , fluid = True


# Callback Section
# --------------------------------------------------------------


"""Data selection"""
# Data selection - Dropdown
@app.callback(
    Input(component_id='dpdn-data-selection', component_property='value'),
    Output(component_id='checklist-data-selection', component_property='value'),
    Output(component_id='data-viewer', component_property='data'),
    Output(component_id='dpdn-col-selection', component_property='options'),
)
def update_data(selected_data):
    """
    need to modify the codes for not only 'df_viewer'
    """
    file_path = data_path + '/' + selected_data
    df_viewer = pd.read_sas(file_path, encoding='iso-8859-1', format='sas7bdat') ##
    df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]  # If you want to check whether it works properly or not, you could make this line as annotation
    df_viewer = df_viewer.loc[:15] # need to remove (This line is for programming speed)
    
    dpdn_col_selection = [{'label':column, 'value':column} for column in (df_viewer.columns)]
    
    return [selected_data], df_viewer.to_dict('records'), dpdn_col_selection

# Data selection - Checklist
# @app.callback(
#     Output(component_id='dpdn-data-selection', component_property='value'),
#     Input(component_id='checklist-data-selection', component_property='value')
# )
# def update_data(selected_data):
#     return selected_data


"""Columns selection""" #-> need to execute pop up
# Columns selection - Dropdown
@app.callback(
    Input(component_id='dpdn-col-selection', component_property='value'),
    Output(component_id='checklist-col-selection', component_property='value'),
)
def update_selected_columns_list(selected_columns):
    print(type(selected_columns[-1])) # Need to execute pop up, why are they all str?
    return selected_columns
# Columns selection - Checklist
@app.callback(
    Input(component_id='checklist-col-selection', component_property='value'),
    Output(component_id='dpdn-col-selection', component_property='value'),
)
def update_selected_columns_list(selected_columns):
    return selected_columns
# # Columns selection - Button (check all columns)
# @app.callback(
#     Input(component_id='btn-col-all', component_property='n_clicks'),
#     Input(component_id='dpdn-col-selection', component_property='options'),
#     Output(component_id='checklist-col-selection', component_property='value'),
# )

# ##### PROBLEMMMMMMM
# def select_all_columns(n_clicks, all_columns):
#     if n_clicks > 0:
#         if n_clicks % 2 == 1:
#             list_columns = [columns['value'] for columns in all_columns]
#         else:
#             list_columns = []
        
#     else:
#         list_columns = [columns['value'] for columns in all_columns]
    
#     return list_columns

# Columns selection - Button (update data viewer)
@app.callback(  # Not optimal
    Output(component_id='data-viewer', component_property='data'),
    Input(component_id='btn-col-update', component_property='n_clicks_timestamp'),
    Input(component_id='dpdn-data-selection', component_property='value'),
    Input(component_id='dpdn-col-selection', component_property='value')
)
def viewer_update(n_clicks_timestamp, selected_data, selected_columns):
    if int(time.time()) - int(n_clicks_timestamp/1000) < 3:
        print(int(n_clicks_timestamp/1000), time.time())
        file_path = data_path + '/' + selected_data
        df_viewer = pd.read_sas(file_path, encoding='iso-8859-1', format='sas7bdat') ##
        df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]  # If you want to check whether it works properly or not, you could make this line as annotation
        df_viewer = df_viewer.loc[:, selected_columns]
        df_viewer = df_viewer.loc[:15] # need to remove (This line is for programming speed)

        return df_viewer.to_dict('records')
    
    else:
        file_path = data_path + '/' + selected_data
        df_viewer = pd.read_sas(file_path, encoding='iso-8859-1', format='sas7bdat') ##
        df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]  # If you want to check whether it works properly or not, you could make this line as annotation
        df_viewer = df_viewer.loc[:15] # need to remove (This line is for programming speed)

        return df_viewer.to_dict('records')



# # @app.callback(
# #     Output(component_id='data-viewer', component_property='data'),
# #     # Input(component_id='btn-col-update', component_property='n_clicks'),
# #     Input(component_id='btn-col-update', component_property='n_clicks_timestamp'),
# #     # Input(component_id='btn-col-update', component_property='n_clicks_previous'),
# #     Input(component_id='dpdn-data-selection', component_property='value'),
# #     Input(component_id='dpdn-col-selection', component_property='value')
# #     )
# # def show_clicks(n_clicks_timestamp, selected_data, selected_columns):
# #     # if n_clicks > n_clicks_previous:
# #     # if int(n_clicks_timestamp) > time.now():
# #     #     file_path = data_path + '/' + selected_data
# #     #     df_viewer = pd.read_sas(file_path, encoding='iso-8859-1', format='sas7bdat') ##
# #     #     df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]  # If you want to check whether it works properly or not, you could make this line as annotation
# #     #     df_viewer = df_viewer.loc[:, selected_columns]
# #     #     df_viewer = df_viewer.loc[:15] # need to remove (This line is for programming speed)
# #     #     print('ey')

# #     #     return df_viewer.to_dict('records')
# #     time.sleep(1)
# #     t = int(time.time())
# #     print(int(n_clicks_timestamp/1000), t)
# #     file_path = data_path + '/' + selected_data
# #     df_viewer = pd.read_sas(file_path, encoding='iso-8859-1', format='sas7bdat') ##
# #     df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]  # If you want to check whether it works properly or not, you could make this line as annotation
# #     df_viewer = df_viewer.loc[:, selected_columns]
# #     df_viewer = df_viewer.loc[:15] # need to remove (This line is for programming speed)
# #     print('ey')

# #     return df_viewer.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)