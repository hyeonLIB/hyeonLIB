import dash
from dash import callback, html
from dash.dependencies import Input, Output

import pandas as pd
import os
from pages import data_import
# import dash_pivottable.dash_pivottable as dash_pivottable
# from dash_pivottable.data import data
# import components

# global data_path
# data_path = './raw_data'
# dir_list = os.listdir(data_path)
# dir_list.sort()
# # Initialize dataframe
# global df_viewer, main_dataframe
# df_viewer = pd.read_sas(f'{data_path}/{dir_list[-1]}', encoding='iso-8859-1', format='sas7bdat')
# df_viewer = df_viewer.rename(columns=str.lower)
# main_dataframe = df_viewer
# df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]
# df_viewer = df_viewer.loc[:15] # need to remove
# df_viewer = df_viewer[['age','sex','region']]
# main_dataframe = df_viewer


# # main_dataframe = data_import.main_dataframe
# pivot_data = main_dataframe.values.tolist()
# col = list(main_dataframe.columns)
# pivot_data.insert(0,col)
# print(pivot_data)


# # layout = []
# layout = html.Div([
#     dash_pivottable.PivotTable(
#         id='table',
#         # data=data,
#         cols=['Day of Week'],
#         colOrder="key_a_to_z",
#         rows=['Party Size'],
#         rowOrder="key_a_to_z",
#         rendererName="Grouped Column Chart",
#         aggregatorName="Average",
#         vals=["Total Bill"],
#         valueFilter={'Day of Week': {'Thursday': False}}
#     ),
#     html.Div(
#         id='output'
#     )
# ])


# @callback(Output('output', 'children'),
#               [Input('table', 'cols'),
#                Input('table', 'rows'),
#                Input('table', 'rowOrder'),
#                Input('table', 'colOrder'),
#                Input('table', 'aggregatorName'),
#                Input('table', 'rendererName')])
# def display_props(cols, rows, row_order, col_order, aggregator, renderer):
#     return [
#         html.P(str(cols), id='columns'),
#         html.P(str(rows), id='rows'),
#         html.P(str(row_order), id='row_order'),
#         html.P(str(col_order), id='col_order'),
#         html.P(str(aggregator), id='aggregator'),
#         html.P(str(renderer), id='renderer'),
#     ]


layout = html.Div([
    html.Div([
        html.Div(className='row1'),
        html.Div(className='row2'),
    ],
    className='app',),
    html.Script(src='PivotTable.js'),
])