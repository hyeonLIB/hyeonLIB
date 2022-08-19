from dash import Dash, dcc, html, Output, Input, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime
import os

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

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
            meta_tags=[{'name': 'viewport',
                        'content': 'width=device-width, initial-scale=1.0'}]
            )

# Layout section: Bootstrap
# --------------------------------------------------------------

app.layout = dbc.Container([
    # Title of the application
    dbc.Row([
        dbc.Col(
            html.H1("국민건강영양조사 분석 대시보드",
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
            dcc.Dropdown(id='dpdn-col-selection', multi=True, value=['PFE','BNTX'],
                        options=[{'label':column, 'value':column} for column in sorted(df_viewer.columns)],  # % sorted ?
                        style = {"margin-bottom":"18px"}),
            dcc.Checklist(
                id="checklist-col-selection",
                options=[{"label": column, "value": column} for column in df_viewer.columns],  
                labelStyle={"display": "block"},
                style={"height":300, "width":415, "overflow":"auto", "fontSize":18, "margin-bottom":"18px"},
                labelClassName='pb-1',
                value=[]),
            html.Button(id='btn-col-selection', n_clicks=0, children="Update")  ## you should place to the right side
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

# # Data selection
# by Dropdown 
@app.callback(
    Output(component_id='checklist-data-selection', component_property='value'),
    Output(component_id='data-viewer', component_property='data'),
    Output(component_id='dpdn-col-selection', component_property='options'),
    Output(component_id='checklist-col-selection', component_property='options'),
    Input(component_id='dpdn-data-selection', component_property='value')
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
    checklist_col_selection = [{'label':column, 'value':column} for column in (df_viewer.columns)]
    
    return [selected_data], df_viewer.to_dict('records'), dpdn_col_selection, checklist_col_selection
# by checklist



# # button for viewer update
# @app.callback(
#     Output(component_id='data-viewer', component_property='data')
#     Input(component_id='btn-col-selection', component_property='n_clicks')
# )
# def viewer_update(n_clicks):
#     return data

# # need to change to multiple checklist -> single
# @app.callback(
#     Output(component_id='dpdn-data-selection', component_property='value'),
#     Input(component_id='checklist-data-selection', component_property='value')
# )
# def update_data(selected_data):
#     return [selected_data]


# **** Done -> need to change to interactive
# # Columns selection
# @app.callback(
#     Output(component_id='checklist-col-selection', component_property='value'),
#     Input(component_id='dpdn-col-selection', component_property='value')
# )
# def update_columns(selected_columns):
#     return selected_columns
# @app.callback(
#     Output(component_id='dpdn-col-selection', component_property='value'),
#     Input(component_id='checklist-col-selection', component_property='value')
# )
# def update_columns(selected_columns):
#     return selected_columns

# Update data viewer

if __name__ == '__main__':
    app.run_server(debug=True)