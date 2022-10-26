import time
from dash import Dash, no_update
from dash_extensions.enrich import MultiplexerTransform, DashProxy, dcc, html, dash_table, Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import datetime
import re
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
    
    return df

def properties_specification(df_viewer, selected_column, type):
    total_data = len(df_viewer)
    missing_data_count = df_viewer.isnull().sum()
    responds_data_count = total_data - missing_data_count
    rate_missing_data_count = missing_data_count/total_data * 100

    if type == 'categorical':
        """
        Categorical
        Specification of property
        클래스
        클래스 수
        클래스별 개체 수
        전체 데이터 수
        관측 수
        결측 수
        결측 비
        """
        name_class = df_viewer[selected_column].unique()
        num_classes = df_viewer[selected_column].nunique()
        num_class = df_viewer[selected_column].value_counts()
        properties = {
            "total_data":total_data,
            "responds_data":responds_data_count[selected_column],
            "missing_data":missing_data_count[selected_column], 
            "missing_data_rate":rate_missing_data_count[selected_column],
            "num_class":num_class,
            "num_classes":num_classes,
            "name_class":name_class
        }
        print("categorical value")
    else:
        """
        Numerical
        Specification of property
        전체 데이터 수
        관측 수
        결측 수
        결측 비
        """
        properties = {
            "total_data":total_data,
            "responds_data":responds_data_count[selected_column],
            "missing_data":missing_data_count[selected_column], 
            "missing_data_rate":rate_missing_data_count[selected_column],
        }
        print("numberable value")
    
    return properties


# Initialize dataframe
df_viewer = pd.read_sas(f'{data_path}/{dir_list[-1]}', encoding='iso-8859-1', format='sas7bdat')
main_dataframe = df_viewer

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
    html.Div(id='tab', children='BigDataAnalysis'),
    dbc.Modal(  
        [
            dbc.ModalHeader(dbc.ModalTitle("변수 속성 명세서"), close_button=True),
            dbc.ModalBody("Initialize"),
            dbc.ModalFooter(
                dbc.Button(
                    "Close",
                    id="close-properties-specification",
                    className="ms-auto",
                    n_clicks=0,
                )
            ),
        ],
        id="modal-properties-specification",
        is_open=False,
        scrollable=True,
        size="lg",
        backdrop=True,
        fade=True,
        centered=True,
    ),


    # Title of the application
    dbc.Row([
        dbc.Col(
            html.H1("국민건강영양조사 분석 대시보드",
                className='text-center text-primary, mb-4',
                style = {"margin-top":"10px"}
            ), # mb-4 -> some padding
        width=12),
    ]),

    dbc.Row([
        # Data selection  * Multiple setting on next version (merge data)
        dbc.Col([
            html.H6(children="Data Selection",
                    className='text-center',),
            dcc.Dropdown(id='dpdn-data-selection', multi=True, value=[dir_list[-1]],
                        options = [{'label':x, 'value':x} for x in dir_list],
                        style = {"margin-bottom":"18px"}),
            dcc.Checklist(
                id="checklist-data-selection",
                options=[{"label": file_name, "value": file_name} for file_name in dir_list],
                labelStyle={"display": "block"},
                style={"height":300, "width":307, "overflow":"auto", "fontSize":18},
                labelClassName='pb-3',
                value=[dir_list[-1]])
        ], width = {'size':3}),
        
        # Columns selection
        dbc.Col([
            html.H6(children="Columns Selection",
                    className='text-center',),
            dcc.Dropdown(id='dpdn-col-selection', multi=True, value=[], # default select all?
                        options=[{'label':column, 'value':column} for column in df_viewer.columns],
                        # optionHeight=120,
                        # style = {'max-height': '150px', 'overflow': 'scroll','margin-bottom':'4px'}),
                        # style = {'margin-bottom':'4px'}),
                        # white-space: nowrap
                        style = {'max-height':'150px','position':'relative','display':'grid','overflow-y': 'auto','margin-bottom':'4px','text-overflow':'ellipsis'}),
            
            dbc.Row(
                [
                    dbc.Col(dbc.Button(id="btn-col-all", color="dark", outline=True, n_clicks=0, children="Select all", className="px-0 py-0 mb-2"), width=4),
                    dbc.Col(dbc.Button(id="btn-col-update", color="dark", outline=True, n_clicks=0, children="Update", className="px-0 py-0 mb-2"), width=2),
                ],
                justify="between",
            ),

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
        ], width = {'size':5}),
        
        dbc.Col([
            html.H6(children="Graph",
                    className='text-center',),
            html.Div(id='container', children=[])
        ], width = {'size':3}), 
    ]),

    # Data viewer
    dbc.Row([
        html.H6(children="Data Viewer",),
        dash_table.DataTable(
            id='data-viewer',
            columns=[{'name': i, 'id':i, 'deletable':True, 'selectable':False} for i in df_viewer.columns],
            data=df_viewer.to_dict('records'),
            virtualization=True,
            filter_action='native',
            fixed_rows={'headers': True},
            style_cell={'minWidth': 70, 'width': 100, 'maxWidth': 140},
            style_table={'height': 400},
        )
    ]),

    dbc.Row(
        dbc.Col(dbc.Button(id="next-page", color="dark", outline=True, n_clicks=0, children="Next", className="mt-4 px-0 py-0 mb-2 justify-content-end"),width={'size':1,'offset':3}), 
        justify="end",
    )

]) # , fluid = True



# Callback Section
# --------------------------------------------------------------

"""Data selection"""
# Data selection - Dropdown
@app.callback(
    Input(component_id='dpdn-data-selection', component_property='value'),
    Output(component_id='checklist-data-selection', component_property='value'),
    Output(component_id='data-viewer', component_property='columns'),
    Output(component_id='data-viewer', component_property='data'),
    Output(component_id='dpdn-col-selection', component_property='options'),
    Output(component_id='dpdn-col-selection', component_property='value')
)
def update_data(selected_datas):
    """
    Need to modify the codes for not only 'df_viewer'
    Prevent Update
    """
    
    global main_dataframe

    main_dataframe = pd.DataFrame()
    df_viewer = pd.DataFrame()
    for selected_data in selected_datas:
        file_path = data_path + '/' + selected_data
        df = pd.read_sas(file_path, encoding='iso-8859-1', format='sas7bdat')
        df_viewer = pd.concat([df_viewer, df.loc[:15]], ignore_index=True) # Need to remove loc[:15]
        main_dataframe = pd.concat([main_dataframe, df], ignore_index=True)

    df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]

    dpdn_col_selection = [{'label':column, 'value':column} for column in (df_viewer.columns)]
    columns = [{'name': i, 'id':i, 'deletable':True} for i in df_viewer.columns]
    
    return selected_datas, columns, df_viewer.to_dict('records'), dpdn_col_selection, []

# Data selection - Checklist
@app.callback(
    Input(component_id='checklist-data-selection', component_property='value'),
    Output(component_id='dpdn-data-selection', component_property='value')
)
def update_data(selected_datas):
    return selected_datas


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
    # State(component_id='', component_property='data'),
    State(component_id='dpdn-col-selection', component_property='value'),
    Output(component_id='data-viewer', component_property='columns'),
    Output(component_id='data-viewer', component_property='data'),
)
def viewer_update(n_clicks, selected_columns):
    if n_clicks is None:
        raise PreventUpdate
    else:
        print(selected_columns)
        if selected_columns == []:
            df_viewer = main_dataframe.loc[:, ~main_dataframe.columns.str.contains("wt_")]
            columns = [{'name': i, 'id':i, 'deletable':True} for i in df_viewer.columns]
            
            return columns, df_viewer.to_dict('records')

        else:
            df_viewer = main_dataframe.loc[:, ~main_dataframe.columns.str.contains("wt_")]
            df_viewer = df_viewer.loc[:, selected_columns]
            columns=[{'name': i, 'id':i, 'deletable':True} for i in df_viewer.columns]

            return columns, df_viewer.to_dict('records')


@app.callback(
    Output(component_id="modal-properties-specification", component_property="children"),
    Output(component_id="container", component_property="children"),
    Input(component_id="table-col-selection", component_property="active_cell"),
    State(component_id="table-col-selection", component_property="data"),
)
def cell_clicked(active_cell, columns_data):
    if active_cell is None:
        return no_update, no_update

    if active_cell["column_id"] == 'col_type':
        row = active_cell['row']
        selected_cell = columns_data[row]
        col_name = selected_cell['col_name']
        col_type = selected_cell['col_type']
        
        selected_column = col_name

        # Categorical variable
        if col_type == 'categorical':

            col_property_info = properties_specification(main_dataframe, selected_column, type=col_type)

            total =         f"  전   체 : {col_property_info['total_data']} "
            responds=       f"  응답수 : {col_property_info['responds_data']} "
            missing=        f"  결측수 : {col_property_info['missing_data']} "
            missing_rate =  f"  결측비 : {round(col_property_info['missing_data_rate'],2)} "
            
            # column propert viewer dataframe -> datatable
            column_property_viewer = [
                {'name':'index','id':'index'},
                {'name':'code_class','id':'code_class'},
                {'name':'name_class','id':'name_class'},
                {'name':'num_class','id':'num_class'},
                {'name':'ratio_class','id':'ratio_class'},
            ]
            """index, name_class, name_class, num_class, num_class/len(total)"""
            data_property_viewer = [
                {'index':i,
                'code_class':col_property_info['name_class'][i],
                'name_class':col_property_info['name_class'][i],
                'num_class':col_property_info['num_class'][i],
                'ratio_class':round(col_property_info['num_class'][i]/col_property_info['total_data'],4)
                } for i in range(col_property_info['num_classes'])
            ]
            
            # Modal component for Variable property sepecification
            modal_children = [
                dbc.ModalHeader(dbc.ModalTitle(f"{selected_column} 속성 명세서"), close_button=True),
                dbc.ModalBody(
                    dbc.Form(
                        [
                            dbc.Row([
                                dbc.Col(
                                    dbc.CardGroup(
                                        [
                                            dash_table.DataTable(
                                                columns = column_property_viewer,
                                                data=data_property_viewer,
                                                virtualization=True,
                                                fixed_rows={'headers': True},
                                                style_cell={'minWidth': 70, 'width': 100, 'maxWidth': 140},
                                                style_as_list_view=True,
                                                style_cell_conditional=[
                                                    {'if': {'column_id': i},
                                                        'textAlign': 'center',
                                                    } for i in ['index']
                                                ],
                                            ),
                                        ],
                                    ), width=9
                                ),

                                dbc.Col(
                                    dbc.ListGroup(
                                        [
                                            dbc.ListGroupItem(total),
                                            dbc.ListGroupItem(responds),
                                            dbc.ListGroupItem(missing),
                                            dbc.ListGroupItem(missing_rate),
                                        ]
                                    ), width=3
                                ),
                            ],),
                        ]
                    ),
                ),
                dbc.ModalFooter(dbc.Button(
                    "Close",
                    id="close-properties-specification",
                    className="ms-auto",
                    n_clicks=0,
                )),
            ]
            
            #graph child fig
            graph_child = html.Div(
                style={'width': '135%', 'display':'inline-block', 'outline':'thin lightgrey solid'},
                children=[
                    dcc.Graph(
                        id = {'type':'class-graph'},
                        figure=px.pie(main_dataframe, names = selected_column, title=selected_column)
                    ),
                ]
            )

            return modal_children, graph_child

        # Numeric variable
        else:
            col_property_info = properties_specification(main_dataframe, selected_column, type=col_type)

            total =         f" 전   체 : {col_property_info['total_data']} "
            responds=       f" 응답수 : {col_property_info['responds_data']} "
            missing=        f" 결측수 : {col_property_info['missing_data']} "
            missing_rate =  f" 결측비 : {round(col_property_info['missing_data_rate'],2)} "

            # Modal component for Variable property sepecification 
            modal_children = [
                dbc.ModalHeader(dbc.ModalTitle(f"{selected_column} 속성 명세서"), close_button=True),
                dbc.ModalBody(dbc.Form(
                        [
                            dbc.Col(
                                dbc.ListGroup(
                                    [
                                        dbc.ListGroupItem(total),
                                        dbc.ListGroupItem(responds),
                                        dbc.ListGroupItem(missing),
                                        dbc.ListGroupItem(missing_rate),
                                    ]
                                ), width=3
                            ),
                        ]
                    ),
                ),
                dbc.ModalFooter(dbc.Button(
                    "Close",
                    id="close-properties-specification",
                    className="ms-auto",
                    n_clicks=0,
                )),
            ]
            
            graph_child = html.Div(
                            style={'width': '135%', 'display':'inline-block', 'outline':'thin lightgrey solid'},
                            children=[
                                dcc.Graph(
                                    id = {'type':'class-graph'},
                                    figure=px.histogram(df_viewer, x=selected_column, color="sex",
                                                        marginal="box", title=selected_column) # or violin, rug
                                                        
                                ),
                            ]
                        )

            return modal_children, graph_child

    else:
        return no_update, no_update

@app.callback(
    Output("modal-properties-specification", "is_open"),
    Input(component_id="table-col-selection", component_property="active_cell"), 
    Input("close-properties-specification", "n_clicks"),
    State("modal-properties-specification","is_open"),
)
def toggle_modal(active_cell, close_n_clicks, is_open):
    if close_n_clicks:
        return not is_open
    if active_cell["column_id"] == 'col_type' and active_cell is not None:
        return True

@app.callback(
    Input(component_id='next-page', component_property='n_clicks'),
    State(component_id='dpdn-col-selection', component_property='value'), ## ***
    State(component_id='data-viewer', component_property='filter_query'),
    Output(component_id='data-viewer', component_property='data'),
)

def data_filtering(n_clicks, selected_columns, query):
    if n_clicks is None:
        return PreventUpdate

    else:
        if query is None:
            if selected_columns != []:
                dataframe = main_dataframe.loc[:, selected_columns]
            else:
                dataframe = main_dataframe

            return no_update

        else:
            dataframe = main_dataframe
            queries = query.split(" && ")
            query_list = []

            for q in queries:
                var = (re.search('{(.*)}', q)).group(1)
                cond = (re.search('} s(.*) ', q)).group(1)
                val = (re.search(f'{cond} (.*)', q)).group(1)
                query_={'var':var, 'cond':cond, 'val':val}
                query_list.append(query_)

            for q in query_list:
                total = len(dataframe)

                if q['cond'] == '=':
                    if 'float' not in str(type(main_dataframe[q['var']][2])): # str
                        val = q['val']
                        dataframe = dataframe.query(f'{q["var"]} == "{val}"')
                        val_count = len(dataframe)
                    else: # float
                        val = np.float64(q['val'])
                        dataframe = dataframe.query(f'{q["var"]} == {val}')
                        val_count = len(dataframe)

                elif q['cond'] == '>': # float
                    val = np.float64(q['val'])
                    dataframe = dataframe.query(f'{q["var"]} > {val}')
                    val_count = len(dataframe)
                
                elif q['cond'] == '>=': # float
                    val = np.float64(q['val'])
                    dataframe = dataframe.query(f'{q["var"]} >= {val}')
                    val_count = len(dataframe)

                elif q['cond'] == '<': # float
                    val = np.float64(q['val'])
                    dataframe = dataframe.query(f'{q["var"]} < {val}')
                    val_count = len(dataframe)

                elif q['cond'] == '<=': # float
                    val = np.float64(q['val'])
                    dataframe = dataframe.query(f'{q["var"]} <= {val}')
                    val_count = len(dataframe)
                
                else:
                    print("e")

                dataframe = dataframe.reset_index(drop=True)
                q['val_count'] = val_count
                q['remainder'] = total - val_count
                total = total - val_count
            

            if selected_columns != []:
                # default_col_list = []
                # default_col_df = dataframe.loc[:, default_col_list]
                selected_col_df = dataframe.loc[:, selected_columns]
                wt_col_df = dataframe.loc[:, main_dataframe.columns.str.contains("wt_")]
                dataframe = pd.concat([selected_col_df, wt_col_df], axis=1)

            print(dataframe)
            print(query_list) # filtered_data dataframe
            
        return no_update

# --------------------------------------------------------------------
# Application RUN

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(debug=True, port=) # If you need to set port number