import dash
# Import necessary libraries 
from dash import no_update, callback
from dash_extensions.enrich import dcc, html, dash_table, Input, Output, State
from dash.exceptions import PreventUpdate
from flask_caching.backends import null
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from tools.tools import load_data, properties_specification, KNHANESPreprocessing
import os
import re

global data_path
data_path = './raw_data'
dir_list = os.listdir(data_path)
dir_list.sort()

# Initialize dataframe
global df_viewer, main_dataframe

try:
    if main_dataframe is not null:
        pass
except NameError: 
    df_viewer = pd.read_sas(f'{data_path}/{dir_list[-1]}', encoding='iso-8859-1', format='sas7bdat')
    df_viewer = df_viewer.rename(columns=str.lower)
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

# Layout

layout = dbc.Container([
    html.Div(id='tab', children='BigDataAnalysis'),
    dcc.Store(id='local',storage_type='local'),
    dcc.Store(id='local2',storage_type='local'),
    dbc.Modal(  
        [
            dbc.ModalHeader(dbc.ModalTitle("변수 속성 명세서"), close_button=True),
            dbc.ModalBody([
                dbc.Row("Initialize"),
                dbc.Row([
                    dbc.Col(
                        [dbc.Button(
                            "변수 타입 변경",
                            id="change-col-type",
                            className="ms-auto px-0 py-0 mb-2",
                            n_clicks=0,
                        )]
                    )
                ],),
            ]),
            dbc.ModalFooter(
                dbc.Button(
                    "Close",
                    id="close-properties-specification",
                    className="ms-auto",
                    n_clicks=0,
                ),
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
                        # style = {'max-height':'150px','position':'relative','display':'grid','overflow-y': 'auto','margin-bottom':'4px','text-overflow':'ellipsis'},
                        style = {'max-height':'150px','margin-bottom':'4px','position':'relative','display':'grid','text-overflow':'ellipsis'},
                        # style = {'overflow-y':'scroll','textOverflow':'ellipsis'}
                        # className="dd-toggle"
            ),
            
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
            html.H6(children="Variable description",
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
@callback(
    Output(component_id="data-viewer", component_property="columns"),
    Output(component_id="data-viewer", component_property="data"),
    Input(component_id="dpdn-data-selection", component_property="value"), # data selection
    Input(component_id="btn-col-update", component_property="n_clicks"), # update button
    State(component_id="dpdn-col-selection", component_property="value"),
)
def data_viewer_update(selected_datas, n_clicks, selected_columns):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    global df_viewer
    global main_dataframe
    if trigger_id == "dpdn-data-selection":
        year_list = [str(int(year))[2:] for year in main_dataframe['year'].unique()]
        for selected_data in selected_datas:
            if selected_data.replace('hn','').replace('_all.sas7bdat','') not in year_list:
                file_path = data_path + '/' + selected_data
                df = pd.read_sas(file_path, encoding='iso-8859-1', format='sas7bdat')	
                df = df.rename(columns=str.lower)
                main_dataframe = pd.concat([main_dataframe, df], ignore_index=True)
                df = df.loc[:, ~df.columns.str.contains("wt_")]
                df_viewer = pd.concat([df_viewer, df.loc[:15]], ignore_index=True) # Need to remove loc[:15]
        sd = [selected_data.replace('hn','').replace('_all.sas7bdat','') for selected_data in selected_datas]
        for year in main_dataframe['year'].unique():
            if str(int(year))[2:] not in sd:
                print("yeah")
                # Would be changed when we use database
                df_viewer = df_viewer[df_viewer.year != year]
                main_dataframe = main_dataframe[main_dataframe.year != year]
        # dataset 다르다.
        # if 2008 in main_dataframe['year'].unique():
        #     main_dataframe = KNHANESPreprocessing(main_dataframe)

        # df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]
        df_columns = [{'name': i, 'id':i, 'deletable':True} for i in df_viewer.columns]
        df_data = df_viewer.to_dict('records')
    elif trigger_id == "btn-col-update":
        if n_clicks is None:
            raise PreventUpdate
        else:
            if selected_columns == []:
                df_columns = [{'name': i, 'id':i, 'deletable':True} for i in df_viewer.columns]
                df_data = df_viewer.to_dict('records')
            elif len(selected_columns) == len(main_dataframe.loc[:, ~main_dataframe.columns.str.contains("wt_")].columns):
                df_viewer = main_dataframe.loc[:, ~main_dataframe.columns.str.contains("wt_")]
                df_columns = [{'name': i, 'id':i, 'deletable':True} for i in df_viewer.columns]
                df_data = df_viewer.to_dict('records')
            else:
                df_viewer = main_dataframe.loc[:, ~main_dataframe.columns.str.contains("wt_")]
                df_viewer = df_viewer.loc[:, selected_columns]
                df_columns=[{'name': i, 'id':i, 'deletable':True} for i in df_viewer.columns]
                df_data = df_viewer.to_dict('records')

    return df_columns, df_data

# Output - Data selection
@callback(
    Output(component_id="checklist-data-selection", component_property="value"),
    Output(component_id="dpdn-data-selection", component_property="value"),
    Input(component_id="checklist-data-selection", component_property="value"),
    Input(component_id="dpdn-data-selection", component_property="value"),
)
def sync_data_selection(checklist_selected_datas, dpdn_selected_datas):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "checklist-data-selection":
        value = checklist_selected_datas
    else:
        value = dpdn_selected_datas
    return value, value

@callback(
    Output(component_id="dpdn-col-selection", component_property="value"),
    Output(component_id="table-col-selection", component_property="selected_rows"),
    Output(component_id="dpdn-col-selection", component_property="options"),
    Output(component_id="table-col-selection", component_property="data"),
    Output(component_id="table-col-selection", component_property="selected_cells"),
    Output(component_id="table-col-selection", component_property="active_cell"),
    Output(component_id="modal-properties-specification", component_property="children"),
    Output(component_id="modal-properties-specification", component_property="size"),
    Output(component_id="modal-properties-specification", component_property="is_open"),
    Output(component_id="close-properties-specification", component_property="n_clicks"),
    Output(component_id="container", component_property="children"),
    Output(component_id="local", component_property="data"),
    Input(component_id="dpdn-col-selection", component_property="value"),
    State(component_id='dpdn-col-selection', component_property='options'),
    Input(component_id="table-col-selection", component_property="derived_virtual_selected_rows"),
    State(component_id="table-col-selection", component_property="derived_virtual_data"),
    Input(component_id="dpdn-data-selection", component_property="value"),
    Input(component_id='btn-col-all', component_property='n_clicks'),
    Input(component_id="change-col-type", component_property='n_clicks'),
    State(component_id="local", component_property="data"),
    Input(component_id="table-col-selection", component_property="active_cell"),
    State(component_id="table-col-selection", component_property="data"),
    Input(component_id="modal-properties-specification", component_property="is_open"),
    Input(component_id="close-properties-specification", component_property="n_clicks"),
    prevent_initial_call=True
)
def sync_callback(selected_columns, options, slctd_row_indices, all_rows_data, selected_data, n_clicks, n_clicks_col_type, query, active_cell, columns_data, is_open, close_n_clicks):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    trigger_property = ctx.triggered[0]["prop_id"].split(".")[1]
    """
    Trigger_id
    (Done)dpdn-col-selection                  :  value
    (Do)table-col-selection                 :  derived_virtual_selected_rows, active_cell
    (Done)dpdn-data-selection                 :  value
    (Done)btn-col-all                         :  n_clicks -> n_clicks_all
    (Done)change-col-type                     :  n_clicks -> n_clicks_change_type
    modal-properties-specification      :  is_open
    close-properties-specification      :  n_clicks -> n_clicks_close
    """

    global df_viewer
    global main_dataframe


    # dpdn-col-selection
    if trigger_id == "dpdn-col-selection":
        options_list = [x['value'] for x in options]
        options_dict = {val : x+1 for x, val in enumerate(options_list)}
        slctd_row_indices = [options_dict[x]-1 for x in selected_columns]
        return selected_columns, slctd_row_indices, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
    # table-col-selection
    elif trigger_id == "table-col-selection":
        if trigger_property == "derived_virtual_selected_rows":
            selected_columns = [all_rows_data[i]['col_name'] for i in slctd_row_indices]
            return selected_columns, slctd_row_indices, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
        elif trigger_property == "active_cell":
            if active_cell is None:
                return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

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
                        dbc.ModalHeader(dbc.ModalTitle(f"{selected_column} 속성 명세서 - {col_type}"), close_button=True),
                        dbc.ModalBody(
                            dbc.Form(
                                [
                                    dbc.Row([
                                        dbc.Col(
                                            [dbc.Button(
                                                "변수 타입 변경",
                                                id="change-col-type",
                                                className="ms-auto px-0 py-0 mb-2",
                                                n_clicks=0,
                                            )]
                                        )
                                    ],),
                                    dbc.Row([
                                        dbc.Col(
                                            dbc.CardGroup(
                                                [
                                                    dash_table.DataTable(
                                                        columns = column_property_viewer,
                                                        data=data_property_viewer,
                                                        virtualization=True,
                                                        fixed_rows={'headers': True},
                                                        style_as_list_view=True,
                                                        style_cell={'minWidth': 50,'width': 110},
                                                        style_cell_conditional=[
                                                            {
                                                                'if': {'column_id': i},
                                                                'textAlign': 'center',
                                                                'width': 50
                                                            } for i in ['index']
                                                        ],
                                                    ),
                                                ],
                                            ), width=6
                                        ),

                                        dbc.Col([
                                            dbc.ListGroup(
                                                [
                                                    dbc.ListGroupItem(total),
                                                    dbc.ListGroupItem(responds),
                                                    dbc.ListGroupItem(missing),
                                                    dbc.ListGroupItem(missing_rate),
                                                ]
                                            ),
                                        ], width=2,),

                                        dbc.Col([
                                            html.Div(
                                                style={'width': '135%', 'display':'inline-block', 'outline':'thin lightgrey solid'},
                                                children=[
                                                    dcc.Graph(
                                                        id = {'type':'class-graph'},
                                                        figure=px.pie(main_dataframe, names = selected_column, title=selected_column)
                                                    ),
                                                ]
                                            ),
                                        ], width=4,),                    
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
                    description = []
                    # return modal_children, no_update, 'xl', {'col_name':selected_column,'col_type':'categorical'}, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
                    return no_update, no_update, no_update, no_update, no_update, no_update, modal_children, 'xl', True, 0, description, {'col_name':selected_column,'col_type':'categorical'}
            # Numeric variable
                else:
                    col_property_info = properties_specification(main_dataframe, selected_column, type=col_type)

                    total =         f" 전   체 : {col_property_info['total_data']} "
                    responds=       f" 응답수 : {col_property_info['responds_data']} "
                    missing=        f" 결측수 : {col_property_info['missing_data']} "
                    missing_rate =  f" 결측비 : {round(col_property_info['missing_data_rate'],2)} "

                    # Modal component for Variable property sepecification 
                    modal_children = [
                        dbc.ModalHeader(dbc.ModalTitle(f"{selected_column} 속성 명세서 - {col_type}"), close_button=True),
                        dbc.ModalBody(
                            dbc.Form(
                                [
                                    dbc.Row([
                                        dbc.Col(
                                            dbc.Button(
                                                "변수 타입 변경",
                                                id="change-col-type",
                                                className="ms-auto px-0 py-0 mb-2",
                                                n_clicks=0,
                                            )
                                        )
                                    ]),
                                    dbc.Row([    
                                        dbc.Col(
                                            dbc.ListGroup(
                                                [
                                                    dbc.ListGroupItem(total),
                                                    dbc.ListGroupItem(responds),
                                                    dbc.ListGroupItem(missing),
                                                    dbc.ListGroupItem(missing_rate),
                                                ]
                                            ), width=4
                                        ),

                                        dbc.Col([
                                                html.Div(
                                                    style={'width': '135%', 'display':'inline-block', 'outline':'thin lightgrey solid'},
                                                    children=[
                                                        dcc.Graph(
                                                            id = {'type':'class-graph'},
                                                            figure=px.histogram(df_viewer, x=selected_column, color="sex",
                                                                                marginal="box", title=selected_column) # or violin, rug
                                                        ),
                                                    ]
                                                ),
                                            ], width=4,
                                        ),
                                    ]),
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
                    description=[]
                    return no_update, no_update, no_update, no_update, no_update, no_update, modal_children, 'lg', True, 0, description, {'col_name':selected_column,'col_type':'numeric'}
            else:
                return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    # dpdn-data-selection
    elif trigger_id == "dpdn-data-selection":
        # only for year of data
        import time
        while len(selected_data) != len(df_viewer['year'].unique()):
            time.sleep(0.1)
        options = [{'label':column, 'value':column} for column in (df_viewer.columns)]
        selected_data=[
            {'col_name':i, 'col_type':'numeric'}
            if 'float' in str(type(df_viewer.iloc[1][i]))
            else {'col_name':i,'col_type':'categorical'
            } for i in df_viewer.columns
        ]
        return selected_columns, slctd_row_indices, options, selected_data, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    # btn-select-all
    elif trigger_id == "btn-col-all":
        if n_clicks is None:
            raise PreventUpdate
        else:
            if n_clicks % 2 == 1:
                selected_columns = [columns['value'] for columns in options]
                slctd_row_indices = list(range(len(options)))
            else:
                selected_columns = []
                slctd_row_indices = []
            return selected_columns, slctd_row_indices, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

   
    
    # button change-col-type
    elif trigger_id == "change-col-type":
        if n_clicks_col_type == 0:
            raise PreventUpdate
        else:
            # global main_dataframe
            if query['col_type'] == 'categorical':
                main_dataframe = main_dataframe.astype({query['col_name']:np.float64})
                print('here')
            else:
                main_dataframe = main_dataframe.astype({query['col_name']:'int32'})
                main_dataframe = main_dataframe.astype({query['col_name']:'str'})
                print('here')
            df_viewer = main_dataframe.loc[:, ~main_dataframe.columns.str.contains("wt_")]
            df_viewer = df_viewer[:15]
            options = [{'label':column, 'value':column} for column in (df_viewer.columns)]
            selected_data=[
                {'col_name':i, 'col_type':'numeric'}
                if 'float' in str(type(df_viewer.iloc[1][i]))
                else {'col_name':i,'col_type':'categorical'
                } for i in df_viewer.columns
            ]
            # if automatically update modal component when click type change button
            return selected_columns, slctd_row_indices, options, selected_data, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    elif trigger_id == 'modal-properties-specification':
        if not is_open:
            return no_update, no_update, no_update, no_update, [], None, no_update, no_update, no_update, no_update, no_update, no_update
        else:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update    

    elif trigger_id == 'close-properties-specification':
        if close_n_clicks == 1:
            return no_update, no_update, no_update, no_update, [], None, no_update, no_update, False, 0, no_update, no_update
        if active_cell["column_id"] == 'col_type' and active_cell is not None:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, True, 0, no_update, no_update

@callback(
    Output(component_id='local2', component_property='data'),
    Input(component_id='next-page', component_property='n_clicks'),
    State(component_id='dpdn-col-selection', component_property='value'), ## ***
    State(component_id='data-viewer', component_property='filter_query'),
)
def data_filtering(n_clicks, selected_columns, query):
    if n_clicks is None:
        return no_update

    else:
        global main_dataframe
        if query is None:
            if len(selected_columns)==len(main_dataframe.columns):
                main_dataframe = main_dataframe
            elif selected_columns != []:
                wt_col_df = main_dataframe.loc[:, main_dataframe.columns.str.contains("wt_")]
                selected_col_df = main_dataframe.loc[:, selected_columns]
                main_dataframe = pd.concat([selected_col_df, wt_col_df], axis=1)
            else:
                main_dataframe = main_dataframe

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
            

            if len(selected_columns) == len(main_dataframe.columns):
                main_dataframe = dataframe
            elif selected_columns != []:
                # default_col_list = []
                # default_col_df = dataframe.loc[:, default_col_list]
                selected_col_df = dataframe.loc[:, selected_columns]
                wt_col_df = dataframe.loc[:, main_dataframe.columns.str.contains("wt_")]
                main_dataframe = pd.concat([selected_col_df, wt_col_df], axis=1)
            else:
                main_dataframe = dataframe

            print(main_dataframe)
            print(query_list) # filtered_data dataframe
            
        return query_list

















Output(component_id='table-col-selection',component_property='selected_rows'),
Output(component_id='checklist-col-selected',component_property='options'),
Output(component_id='checklist-col-selected', component_property='value'),
Output(component_id="modal-properties-specification", component_property="children"),
Output(component_id="modal-properties-specification", component_property="size"),
Output(component_id="modal-properties-specification", component_property="is_open"),
Output(component_id="close-properties-specification", component_property="n_clicks"),
Output(component_id='local',component_property='data'),
Output(component_id="table-col-selection", component_property="data"),
Output(component_id="table-col-selection", component_property="selected_cells"),
Output(component_id="table-col-selection", component_property="active_cell"),