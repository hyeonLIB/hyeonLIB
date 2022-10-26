# data viewer

# import dash
# # Import necessary libraries 
from dash import no_update, callback
from dash_extensions.enrich import dcc, html, dash_table, Input, Output, State
# from dash.exceptions import PreventUpdate
# from flask_caching.backends import null
# import plotly.express as px
import dash_bootstrap_components as dbc
# import pandas as pd
# import numpy as np
# from tools.tools import load_data, properties_specification, KNHANESPreprocessing
# import os
# import re


# def viewer_table(main_dataframe):
#     data_viewer = dbc.Row([
#         html.H6(children="Data Viewer",),
#         dash_table.DataTable(
#             id='data-viewer',
#             columns=[{'name': i, 'id':i, 'deletable':True, 'selectable':False} for i in main_dataframe.columns],
#             data=main_dataframe.to_dict('records'),
#             virtualization=True,
#             filter_action='native',
#             fixed_rows={'headers': True},
#             style_cell={'minWidth': 70, 'width': 100, 'maxWidth': 140},
#             style_table={'height': 400},
#         )
#     ])
#     return data_viewer

# from pages.data_import1 import main_dataframe
# data_viewer = viewer_table(main_dataframe)

layout = dbc.Container([
    # dcc.Store(id='filtering-query',storage_type='local'),
    # dbc.Row([
    #     dbc.Col(
    #         html.H1("국민건강영양조사 분석 대시보드",
    #             className='text-center text-primary, mb-4',
    #             style = {"margin-top":"10px"}
    #         ), # mb-4 -> some padding
    #     width=12),
    # ]),
    # data_viewer,
    # dbc.Row(
    #     dbc.Col(dbc.Button(id="next-page1", color="dark", outline=True, n_clicks=0, children="Next", className="mt-4 px-0 py-0 mb-2 justify-content-end"),width={'size':1,'offset':3}), 
    #     justify="end",
    # )
])


# @callback(
#     Output(component_id='filtering-query', component_property='data'),
#     # Input(component_id='next-page', component_property='n_clicks'),
#     Input(component_id='next-page1', component_property='filter_query'),
#     Input(component_id='item-3', component_property='n_clicks'),
# )
@callback(
    Output(component_id='filring-query', component_property='data'),
    # Input(component_id='next-page', component_property='n_clicks'),
    Input(component_id='n-page1', component_property='filter_query'),
    Input(component_id='it3', component_property='n_clicks'),
)
def check(n_clicks):
    print(n_clicks)
    return no_update

# @callback(
#     Output(component_id='filtering-query', component_property='data'),
#     Input(component_id='next-page', component_property='n_clicks'),
#     State(component_id='data-viewer', component_property='filter_query'),
# )
# def data_filtering(n_clicks, query):
#     print('callback works?')
#     if n_clicks is None:
#         print('hre')
#         return no_update

#     else:
#         print("heya")
#         global main_dataframe
#         if query is None:
#             return no_update

#         else:
#             dataframe = main_dataframe
#             queries = query.split(" && ")
#             query_list = []

#             for q in queries:
#                 var = (re.search('{(.*)}', q)).group(1)
#                 cond = (re.search('} s(.*) ', q)).group(1)
#                 val = (re.search(f'{cond} (.*)', q)).group(1)
#                 query_={'var':var, 'cond':cond, 'val':val}
#                 query_list.append(query_)

#             for q in query_list:
#                 total = len(dataframe)

#                 if q['cond'] == '=':
#                     if 'float' not in str(type(main_dataframe[q['var']][2])): # str
#                         val = q['val']
#                         dataframe = dataframe.query(f'{q["var"]} == "{val}"')
#                         val_count = len(dataframe)
#                     else: # float
#                         val = np.float64(q['val'])
#                         dataframe = dataframe.query(f'{q["var"]} == {val}')
#                         val_count = len(dataframe)

#                 elif q['cond'] == '>': # float
#                     val = np.float64(q['val'])
#                     dataframe = dataframe.query(f'{q["var"]} > {val}')
#                     val_count = len(dataframe)
                
#                 elif q['cond'] == '>=': # float
#                     val = np.float64(q['val'])
#                     dataframe = dataframe.query(f'{q["var"]} >= {val}')
#                     val_count = len(dataframe)

#                 elif q['cond'] == '<': # float
#                     val = np.float64(q['val'])
#                     dataframe = dataframe.query(f'{q["var"]} < {val}')
#                     val_count = len(dataframe)

#                 elif q['cond'] == '<=': # float
#                     val = np.float64(q['val'])
#                     dataframe = dataframe.query(f'{q["var"]} <= {val}')
#                     val_count = len(dataframe)
                
#                 else:
#                     print("e")

#                 dataframe = dataframe.reset_index(drop=True)
#                 q['val_count'] = val_count
#                 q['remainder'] = total - val_count
#                 total = total - val_count
            

#             # if len(selected_columns) == len(main_dataframe.columns):
#             #     main_dataframe = dataframe
#             # elif selected_columns != []:
#             #     # default_col_list = []
#             #     # default_col_df = dataframe.loc[:, default_col_list]
#             #     selected_col_df = dataframe.loc[:, selected_columns]
#             #     wt_col_df = dataframe.loc[:, main_dataframe.columns.str.contains("wt_")]
#             #     main_dataframe = pd.concat([selected_col_df, wt_col_df], axis=1)
#             # else:
#             #     main_dataframe = dataframe
#             print(dataframe)
#             # print(main_dataframe)
#             print(query_list) # filtered_data dataframe
            
#         return query_list