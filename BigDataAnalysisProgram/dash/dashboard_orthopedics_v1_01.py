import time
from dash import Dash, no_update
from dash_extensions.enrich import MultiplexerTransform, DashProxy, dcc, html, dash_table, Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
import os
import io

"""

1. Test file -> df_viewer.loc[:15] <remove the line>
2. dcc.Dropdown(id='dpdn-data-selection', multi=False, value=dir_list[-1], 
    -> need to change multiple selection mode and make function can merge the selected year of dataframes
3. auto width of data-viewer cells
4. Do I need to set default columns for data selection part? Then what columns would I do?
5. need to change the component of columns selection dropdown to using scroll method <layout>
    -> It's not comfortable to read the data like it would have too long scroll bar when I select all columns

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

def properties_specification(df_viewer, selected_column):
    total_data = len(df_viewer)
    missing_data_count = col_property.isnull().sum()
    responds_data_count = total_data - missing_data_count
    rate_missing_data_count = missing_data_count/total_data * 100

    if type(df_viewer.loc[1,selected_column])==str:
        properties = {
            "total_data":f"{total_data}",
            "responds_data":f"{responds_data_count[selected_column]}",
            "missing_data":f"{missing_data_count[selected_column]}", 
            "missing_data_rate":f"{rate_missing_data_count[selected_column]}%"
            "class"
        }
        print("categorical value")
    else:
        properties = {
            "total_data":f"{total_data}",
            "responds_data":f"{responds_data_count[selected_column]}",
            "missing_data":f"{missing_data_count[selected_column]}", 
            "missing_data_rate":f"{rate_missing_data_count[selected_column]}%"
        }
        print("numberable value")
    
    return properties


# Initialize dataframe
df_viewer = pd.read_sas('hn19_all.sas7bdat', encoding='iso-8859-1', format='sas7bdat') ##
global col_property
col_property = df_viewer

df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]
df_viewer = df_viewer.loc[:15] # need to remove

# Application
# -------------------------------------------------------------
"""
transforms=[MultiplexerTransform()]
    - Was problem : Default -> A component can have output from only ONE other component
    - Solved by using above method
prevent_initial_callbacks=True
    - For the speed of load data have been initialized
    - It prevents callback functions are activated while on processing classes of component on the app layout are instantiated.
"""
app = DashProxy(__name__, prevent_initial_callbacks=True, transforms=[MultiplexerTransform()],external_stylesheets=[dbc.themes.BOOTSTRAP],
            meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}])

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
        # Data selection  * Multiple setting on next version (merge data)
        dbc.Col([
            dcc.Dropdown(id='dpdn-data-selection', multi=False, value=dir_list[-1],  # need to change to multiple selection mode
                        options = [{'label':x, 'value':x} for x in dir_list],
                        style = {"margin-bottom":"18px"}),
            # dcc.Checklist(
            #     id="checklist-data-selection",
            #     options=[{"label": file_name, "value": file_name} for file_name in dir_list],
            #     labelStyle={"display": "block"},
            #     style={"height":300, "width":415, "overflow":"auto", "fontSize":18},
            #     labelClassName='pb-3',
            #     value=[''])

            dcc.RadioItems( # -> need to change to checklist that can offer dataframe merge
                id="radiobtn-data-selection",
                options=[{"label": file_name, "value": file_name} for file_name in dir_list],
                labelStyle={"display": "block"},
                style={"height":300, "width":415, "overflow":"auto", "fontSize":18},
                labelClassName='pb-3',
                value=dir_list[-1]
            )
            
            ], width = {'size':3}
        ),
        
        # Columns selection
        dbc.Col([
            dcc.Dropdown(id='dpdn-col-selection', multi=True, value=[], # default select all?
                        options=[{'label':column, 'value':column} for column in df_viewer.columns],  # % sorted ?
                        style = {"margin-bottom":"18px"}),

            html.Button(id='btn-col-all', n_clicks=0, children="Select all", style={"margin-right":"370px", "margin-bottom":"10px"}),
            html.Button(id='btn-col-update', n_clicks=0, n_clicks_timestamp=0, children="Update"),  ## you should place to the right side

            dash_table.DataTable(
                id='table-col-selection',
                columns=[{'name':'col_name','id':'col_name'},{'name':'col_type','id':'col_type'}],
                data=[
                    {'col_name':i, 'col_type':'numeric'}
                    if 'float' in str(type(df_viewer.iloc[1][i]))
                    else {'col_name':i,'col_type':'categorical'
                    } for i in df_viewer.columns
                ],
                virtualization=True,
                row_selectable='multi',
                selected_rows=[],
                fixed_rows={'headers': True},
                style_cell={'minWidth': 70, 'width': 100, 'maxWidth': 140, 'padding-right': '30px'},
                style_data={'whiteSpace':'normal', 'height':'auto'},
                # style_cell={"autoWidth":True}, # need to find some other method for adjust auto width
                style_table={'height': 300, 'margin-bottom':'15px'},
                style_cell_conditional=[
                    {'if': {'column_id': i},
                        'textAlign': 'left',
                        'padding-left' : '20px', 
                    } for i in ['col_name']
                ],
                style_as_list_view=True,
                page_action='none',
            ),
        ], 
        width = {'size':5}
        ),

        # Properties of columns
        dbc.Col(
            # [html.H4(
            #     id = 'text-col-property1',
            #     children='',
            #     className='text-right text-primary, mb-4',
            #     # className='mb-4',
            #     style = {"margin-top":"10px"}), # mb-4 -> some padding
            # html.H4(
            #     id = 'text-col-property2',
            #     children='',
            #     className='text-right text-primary, mb-4',
            #     # className='mb-4',
            #     style = {"margin-top":"10px"}),
            # html.H4(
            #     id = 'text-col-property3',
            #     children='',
            #     className='text-right text-primary, mb-4',
            #     # className='mb-4',
            #     style = {"margin-top":"10px"}),
            # html.H4(
            #     id = 'text-col-property4',
            #     children='',
            #     className='text-right text-primary, mb-4',
            #     # className='mb-4',
            #     style = {"margin-top":"10px"})
            # ]
            [html.Br(),
            html.Div(id='container'),]
            ,width=4
        ),
        ]),

    # Data viewer
    dbc.Row([ 
        dash_table.DataTable(
            id='data-viewer',
            columns=[{'name': i, 'id':i, 'deletable':True, 'selectable':False} for i in df_viewer.columns],
            data=df_viewer.to_dict('records'),
            virtualization=True,
            filter_action='native',
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
    # Output(component_id='checklist-data-selection', component_property='value'),
    Output(component_id='radiobtn-data-selection', component_property='value'),
    Output(component_id='data-viewer', component_property='data'),
    Output(component_id='dpdn-col-selection', component_property='options')
)
def update_data(selected_data):
    """
    Need to modify the codes for not only 'df_viewer'
    Prevent Update
    """
    file_path = data_path + '/' + selected_data
    df_viewer = pd.read_sas(file_path, encoding='iso-8859-1', format='sas7bdat')
    
    global col_property 
    col_property = df_viewer

    df_viewer = df_viewer.loc[:3]
    df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]

    dpdn_col_selection = [{'label':column, 'value':column} for column in (df_viewer.columns)]
    
    """
    Will be aboarted
    # global col_property
    # col_property = df_viewer
    # import io
    # buffer = io.StringIO()
    # col_property.info(verbose=False, buf=buffer, memory_usage="deep")
    # print(buffer.getvalue())
    # print(type(buffer.getvalue()))
    """
    return selected_data, df_viewer.to_dict('records'), dpdn_col_selection

# Data selection - Checklist
@app.callback(
    # Input(component_id='checklist-data-selection', component_property='value'),
    Input(component_id='radiobtn-data-selection', component_property='value'),
    Output(component_id='dpdn-data-selection', component_property='value')
)
def update_data(selected_data):
    return selected_data


"""Columns selection""" # 3 -> need to execute pop up
# Columns selection - Dropdown
@app.callback(
    Input(component_id='dpdn-col-selection', component_property='value'),
    State(component_id='dpdn-col-selection', component_property='options'),
    Output(component_id='table-col-selection', component_property='selected_rows'),

)
def update_selected_columns_list(selected_columns, options):
    options_list = [x['value'] for x in options]
    options_dict = {val : x+1 for x, val in enumerate(options_list)}
    selected_columns_index = [options_dict[x]-1 for x in selected_columns]

    return selected_columns_index


# Columns selection - Table
@app.callback(
    Output(component_id='dpdn-col-selection', component_property='value'),
    Input(component_id='table-col-selection', component_property='derived_virtual_data'),
    Input(component_id='table-col-selection', component_property='derived_virtual_selected_rows'),
)
def update_bar(all_rows_data, slctd_row_indices):

    selected_columns = [all_rows_data[i]['col_name'] for i in slctd_row_indices]

    return selected_columns



# # Columns selection - Dropdown
# @app.callback(
#     Input(component_id='dpdn-col-selection', component_property='value'),
#     # Output(component_id='table-col-selection', component_property='value'),
#     Output(component_id='table-col-selection', component_property='derived_virtual_selected_rows'),
#     Output(component_id='text-col-property1', component_property='children'),
#     Output(component_id='text-col-property2', component_property='children'),
#     Output(component_id='text-col-property3', component_property='children'),
#     Output(component_id='text-col-property4', component_property='children')
# )
# def update_selected_columns_list(selected_columns):
#     # different layout if the type is different
#     if len(selected_columns) > 0:
#         selected_column = selected_columns[-1] # col_property

#         col_property_info = properties_specification(col_property, selected_column)

#         """
#         # Specification property
#         total
#         responds
#         missing
#         missing rate
#         """
#         # to text!
#         """
#         전체
#         응답수
#         결측수
#         결측비
#         """
#         total =         f"| 전  체        {col_property_info['total_data']}"
#         responds=       f"| 응답수        {col_property_info['responds_data']}"
#         missing=        f"| 결측수        {col_property_info['missing_data']}"
#         missing_rate =  f"| 결측비        {col_property_info['missing_data_rate']}"
        
#         return selected_columns, total, responds, missing, missing_rate
#     else:    
#         return selected_columns, '','','',''


# Columns selection - Button (check all columns)
@app.callback(
    Input(component_id='btn-col-all', component_property='n_clicks'),
    State(component_id='dpdn-col-selection', component_property='options'),
    Output(component_id='dpdn-col-selection', component_property='value'),
)
def select_all_columns(n_clicks, all_columns):
    if n_clicks is None:
        raise PreventUpdate
    else:
        if n_clicks % 2 == 1:
            list_columns = [columns['value'] for columns in all_columns]
        else:
            list_columns = []

        return list_columns

# Columns selection - Button (update data viewer)
@app.callback(
    Input(component_id='btn-col-update',component_property='n_clicks'),
    State(component_id='dpdn-data-selection', component_property='value'),
    State(component_id='dpdn-col-selection', component_property='value'),
    Output(component_id='data-viewer', component_property='columns'),
    Output(component_id='data-viewer', component_property='data'),
)
def viewer_update(n_clicks, selected_data, selected_columns):
    if n_clicks is None:
        raise PreventUpdate
    else:
        if selected_columns == []:
            file_path = data_path + '/' + selected_data
            df_viewer = pd.read_sas(file_path, encoding='iso-8859-1', format='sas7bdat') ##
            df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]  # If you want to check whether it works properly or not, you could make this line as annotation
        else:
            file_path = data_path + '/' + selected_data
            df_viewer = pd.read_sas(file_path, encoding='iso-8859-1', format='sas7bdat') ##
            df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]  # If you want to check whether it works properly or not, you could make this line as annotation
            df_viewer = df_viewer.loc[:, selected_columns] # ##
            df_viewer = df_viewer.loc[:15] # need to remove (This line is for programming speed)
            columns=[{'name': i, 'id':i, 'deletable':True, 'selectable':False} for i in df_viewer.columns]

        return columns, df_viewer.to_dict('records')





# """Columns selection""" # 3 -> need to execute pop up
# # Columns selection - Dropdown
# @app.callback(
#     Input(component_id='dpdn-col-selection', component_property='value'),
#     State(component_id='dpdn-col-selection', component_property='options'),
#     # Output(component_id='table-col-selection', component_property='value'),
#     # Output(component_id='table-col-selection', component_property='derived_virtual_selected_rows'),
#     Output(component_id='table-col-selection', component_property='selected_rows')

# )
# def update_selected_columns_list(selected_columns, options):
#     options_list = [x['value'] for x in options]
#     options_dict = {val : x+1 for x, val in enumerate(options_list)}
#     selected_columns_index = [options_dict[x]-1 for x in selected_columns]
#     print(selected_columns_index)
#     # selected_columns_index = [3]

#     return selected_columns_index



# @app.callback(
#     # Output(component_id='container', component_property='children'),
#     Output(component_id='dpdn-col-selection', component_property='value'),
#     Input(component_id='table-col-selection', component_property='derived_virtual_data'),
#     Input(component_id='table-col-selection', component_property='derived_virtual_selected_rows'),
#     # Input(component_id='table-col-selection', component_property='active_cell'),
#     # Input(component_id='table-col-selection', component_property='selected_cells')
# )
# def update_bar(all_rows_data, slctd_row_indices):
#             # actv_cell, slctd_cell):
#     # print('***************************************************************************')
#     # print(f'derived_virtual_data \n{all_rows_data}')
#     # print('***************************************************************************')
#     # print(f'slctd_row_indices \n{slctd_row_indices}')
#     # print('***************************************************************************')
#     # print(f'actv_cell \n{actv_cell}')
#     # print('***************************************************************************')
#     # print(f'slctd_cell \n{slctd_cell}')

#     e = [all_rows_data[i]['col_name'] for i in slctd_row_indices]

#     # print(e)
#     return e
#     # dff = pd.DataFrame(all_rows_data)

#     # # used to highlight selected countries on bar chart
#     # colors = ['#7FDBFF' if i in slctd_row_indices else '#0074D9'
#     #           for i in range(len(dff))]

#     # if "country" in dff and "did online course" in dff:
#     #     return [
#     #         dcc.Graph(id='bar-chart',
#     #                   figure=px.bar(
#     #                       data_frame=dff,
#     #                       x="country",
#     #                       y='did online course',
#     #                       labels={"did online course": "% of Pop took online course"}
#     #                   ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
#     #                   .update_traces(marker_color=colors, hovertemplate="<b>%{y}%</b><extra></extra>")
#     #                   )
#     #     ]




# --------------------------------------------------------------------
# Application RUN

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(debug=False) 
    # app.run_server(debug=True, port=) # If you need to set port number