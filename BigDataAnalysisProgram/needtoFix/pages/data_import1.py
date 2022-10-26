# data selection

# Import necessary libraries 
import dash
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
from components.data_import_component import *

# dash.register_page(__name__, path='/data_import1')

# Layout Section
# ----------------------------------------------------------------------------------------------------
major_class = ['list1','list2','list3','list4','list5']
minor_class = ['list1','list2','list3','list4','list5','list6']

major_class_checklist_component = major_class_checklist(major_class)
property_specification_modal_component = property_specification_modal()

layout = dbc.Container([
    dcc.Store(id='__init__',storage_type='local'),
    dcc.Store(id='local', storage_type='local'),
    property_specification_modal_component,
    dbc.Row([
        dbc.Col(
            html.H1("국민건강영양조사 분석 대시보드",
                className='text-center text-primary, mb-4',
                style = {"margin-top":"10px"}
            ), # mb-4 -> some padding
        width=12),
    ]),

    dbc.Row([
        dbc.Col([
            html.H6(children="대분류",className='text-center',),
            major_class_checklist_component,
            ], width={'size':3}),
        dbc.Col([
            html.Div(id='title-minor-class-selection', children=[]),
            html.Div(id='minor-class-selection', children=[],),
            ], width={'size':6}),
        dbc.Col([
            html.Div(id='title-year-selection', children=[]),
            html.Div(id='year-selection', children=[],),
        ], width={'size':3}),
    ]),

    dbc.Row([
        dbc.Col([
            html.Div(id='title-col-selection', children=[]),
            html.Div(id='col-selection', children=[],),], width={'size':6}),
        dbc.Col([
            html.Div(id='title-col-selected', children=[]),
            html.Div(id='col-selected', children=[],),], width={'size':4}),
    ], justify="between"),
    dbc.Row([
        dbc.Col(html.Div(id='extract', children=[]),
        width={'size':1,'offset':3},),
    ],justify="end",),
])




# Callback Section
# ----------------------------------------------------------------------------------------------------
@callback(
    Output(component_id='title-minor-class-selection', component_property='children'),
    Output(component_id='minor-class-selection', component_property='children'),
    Input(component_id='checklist-major', component_property='value'),
    prevent_initial_call=True,
)
def select_major_class(selected_major_class):
    if selected_major_class == []:
        return [], []

    else:
        title_minor_class_component = html.H6(children="소분류",className='text-center',),
        minor_class = ['list1','list2','list3','list4','list5','list6']
        minor_class_component = minor_class_checklist(minor_class)
        return title_minor_class_component, minor_class_component


@callback(
    Output(component_id='title-year-selection', component_property='children'),
    Output(component_id='year-selection', component_property='children'),
    Input(component_id='checklist-minor', component_property='value'),
    prevent_initial_call=True,
)
def select_minor_class(selected_minor_class):
    if selected_minor_class == []:
        return [], []

    else:
        title_year_component = html.H6(children="연도선택",className='text-center',),
        year_list = ['2008','2009','2010','2011']
        year_component = year_selection_checklist(year_list)
        return title_year_component, year_component


# function - load data
@callback(
    Output(component_id='title-col-selection',component_property='children'),
    Output(component_id='col-selection',component_property='children'),
    Output(component_id='title-col-selected',component_property='children'),
    Output(component_id='col-selected',component_property='children'),
    Output(component_id='extract',component_property='children'),
    Input(component_id='checklist-year',component_property='value'),
    State(component_id='checklist-major',component_property='value'),
    State(component_id='checklist-minor',component_property='value'),
    prevent_initial_call=True,
)
def select_year(yearlist, major_list, minor_list):
    if yearlist == []:
        return [], [], [], [], []

    else:
        global main_dataframe
        data_path = './raw_data'
        dir_list = os.listdir(data_path)
        dir_list.sort()
        
        ## data load!
        main_dataframe = pd.read_sas(f'{data_path}/{dir_list[-1]}', encoding='iso-8859-1', format='sas7bdat')
        # print(main_dataframe)
        title_select_columns_component = html.H6(children="Varaible Selection",className='text-center',),
        select_columns_component = select_variable_table(main_dataframe)
        title_selected_columns_component = html.H6(children="Selected Variables",className='text-center',),
        selected_columns_component = selected_variable_checklist()
        extract_button_component = dbc.Button(id="button-extraction", color="dark", outline=True, n_clicks=0, children="EXTRACT", className="mt-4 px-0 py-0 mb-2 justify-content-end")
        return title_select_columns_component, select_columns_component, title_selected_columns_component, selected_columns_component, extract_button_component


# circular sync state
@callback(
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
    Input(component_id='table-col-selection',component_property='derived_virtual_selected_rows'),
    State(component_id='table-col-selection',component_property='derived_virtual_data'),
    Input(component_id='checklist-col-selected',component_property='value'),
    State(component_id='checklist-col-selected',component_property='options'),
    Input(component_id="table-col-selection", component_property="active_cell"),
    State(component_id="table-col-selection", component_property="data"),
    Input(component_id="modal-properties-specification", component_property="is_open"),
    Input(component_id="close-properties-specification", component_property="n_clicks"),
    # Input(component_id='btn-col-all', component_property='n_clicks'),
    Input(component_id="change-col-type", component_property='n_clicks'),
    Input(component_id='local',component_property='data'),
    prevent_initial_call=True,
)
def select_columns(slctd_row_indices, all_rows_data, deleted_column, selected_columns, active_cell, columns_data, is_open, close_n_clicks, change_n_clicks, current_column):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    trigger_property = ctx.triggered[0]["prop_id"].split(".")[1]
    global main_dataframe

    if trigger_id == 'checklist-col-selected':
        if len(deleted_column) == 1:
            idx = 0
            d_index = 0
            for c in selected_columns:
                if c['label'] == deleted_column[0]:
                    d_index = idx
                idx += 1
            del selected_columns[d_index]
            del slctd_row_indices[d_index]
            del deleted_column[0]
            return slctd_row_indices, selected_columns, deleted_column, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    elif trigger_id == 'table-col-selection':
        if trigger_property == 'derived_virtual_selected_rows':
            if slctd_row_indices is None:
                raise PreventUpdate
            
            else:
                selected_columns = [all_rows_data[i]['col_name'] for i in slctd_row_indices]
                selected_columns = [{'label': col, 'value': col} for col in selected_columns]
                return slctd_row_indices, selected_columns, deleted_column, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
        
        elif trigger_property == "active_cell":
            if active_cell is None:
                raise PreventUpdate
            
            if active_cell["column_id"] == 'col_type':
                row = active_cell['row']
                selected_cell = columns_data[row]
                col_name = selected_cell['col_name']
                col_type = selected_cell['col_type']

                # Categorical variable
                if col_type == 'categorical':
                    col_property_info = properties_specification(main_dataframe, col_name, type=col_type)
                    modal_children = properties_specification_component(main_dataframe, col_property_info, col_name, col_type)
                    return no_update, no_update, no_update, modal_children, 'xl', True, 0, {'col_name':col_name,'col_type':'categorical'}, no_update, no_update, no_update
                # Numeric variable
                else:
                    col_property_info = properties_specification(main_dataframe, col_name, type=col_type)
                    modal_children = properties_specification_component(main_dataframe, col_property_info, col_name, col_type)
                    return no_update, no_update, no_update, modal_children, 'lg', True, 0, {'col_name':col_name,'col_type':'numeric'}, no_update, no_update, no_update
            
            else:
                raise PreventUpdate
    
    elif trigger_id == 'change-col-type':
        if change_n_clicks == 0:
            raise PreventUpdate
        else:
            # global main_dataframe
            if current_column['col_type'] == 'categorical':
                # Categorical variable will be changed to numeric
                main_dataframe = main_dataframe.astype({current_column['col_name']:np.float64})
                changed_data=[
                    {'col_name':i, 'col_type':'numeric'}
                    if 'float' in str(type(main_dataframe.iloc[1][i]))
                    else {'col_name':i,'col_type':'categorical'
                    } for i in main_dataframe.columns
                ]
                col_property_info = properties_specification(main_dataframe, current_column['col_name'], 'numeric')
                modal_children = properties_specification_component(main_dataframe, col_property_info, current_column['col_name'], 'numeric')
                return no_update, no_update, no_update, modal_children, 'lg', True, 0, {'col_name':current_column['col_name'],'col_type':'numeric'}, changed_data, no_update, no_update
            else:
                # Numeric variable will be changed to categorical
                main_dataframe = main_dataframe.astype({current_column['col_name']:'int32'})
                main_dataframe = main_dataframe.astype({current_column['col_name']:'str'})
                changed_data=[
                    {'col_name':i, 'col_type':'numeric'}
                    if 'float' in str(type(main_dataframe.iloc[1][i]))
                    else {'col_name':i,'col_type':'categorical'
                    } for i in main_dataframe.columns
                ]
                col_property_info = properties_specification(main_dataframe, current_column['col_name'], 'categorical')
                modal_children = properties_specification_component(main_dataframe, col_property_info, current_column['col_name'], 'categorical')
                return no_update, no_update, no_update, modal_children, 'xl', True, 0, {'col_name':current_column['col_name'],'col_type':'categorical'}, changed_data, no_update, no_update
    
    elif trigger_id == 'modal-properties-specification':
        if not is_open:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, [], None, 
        else:
            raise PreventUpdate
            
    elif trigger_id == 'close-properties-specification':
        if close_n_clicks == 1:
            return no_update, no_update, no_update,  no_update, no_update, False, 0, no_update, no_update, [], None,
        if active_cell["column_id"] == 'col_type' and active_cell is not None:
            return no_update, no_update, no_update, no_update, no_update, True, 0, no_update, no_update, no_update, no_update

    raise PreventUpdate


@callback(
    Output(component_id='__init__',component_property='data'),
    Input(component_id='button-extraction',component_property='n_clicks'),
    State(component_id='checklist-col-selected',component_property='options'),
    State(component_id='checklist-year',component_property='value'),
    prevent_initial_call=True,
)

def extract_data(n_clicks, selected_columns, year_list):
    if n_clicks is None:
        return no_update

    elif n_clicks >= 1:
        selected_columns = [column['label'] for column in selected_columns]
        global main_dataframe
        main_dataframe = main_dataframe.loc[:,selected_columns]
        # print(main_dataframe)
        return {'has_been_init':1}