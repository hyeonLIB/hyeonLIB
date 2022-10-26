# from pages import data_import
# import dash
# from dash_extensions.enrich import dcc, html, dash_table, Input, Output, State
# import dash_bootstrap_components as dbc
# from dash import no_update, callback
# import plotly.express as px
# import pandas as pd
# import numpy as np

# main_dataframe = data_import.main_dataframe

# layout = dbc.Container([
#     dbc.Row([
#         dbc.Col([
            
#             dbc.DropdownMenu(
#                 [
#                     dbc.DropdownMenuItem("성별", id='item-1'),
#                     dbc.DropdownMenuItem(divider=True),
#                     dbc.DropdownMenuItem("연령별", id='item-2'),
#                     dbc.DropdownMenuItem(divider=True),
#                     dbc.DropdownMenuItem("타겟별", id='item-3'),
#                 ],
#                 id = 'dpdn-filtering-options',
#                 label="filtering",
#                 className="m-1",
#                 align_end=False,
#                 direction="end",
#                 toggle_style={
#                     # "textTransform": "uppercase",
#                     "background": "#007bff",
#                 },
#                 toggleClassName="fst-italic border border-dark",
#             )
#         ], width= {'size':2},)
#     ])
# ])


# @callback(
#     Output(component_id='dpdn-filtering-options', component_property='label'),
#     Input(component_id='item-1', component_property='n_clicks'),
#     Input(component_id='item-2', component_property='n_clicks'),
#     Input(component_id='item-3', component_property='n_clicks'),
# )
# def change_label_filtering(n1, n2, n3):
#     ctx = dash.callback_context

#     if (n1 is None and n2 is None and n3 is None) or not ctx.triggered:
#         return "filtering"
    
#     button_id = ctx.triggered[0]["prop_id"].split(".")[0]
#     id_lookup = {"item-1":"성별", "item-2":"연령별", "item-3":"타겟별"}
#     return id_lookup[button_id]


# # data viewer

import dash
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

# dash.register_page(__name__, path='/dashboard')

def viewer_table(main_dataframe):
    if len(main_dataframe) == 0:
        data_viewer = []
    else:    
        data_viewer = dbc.Row([
            html.H6(children="Data Viewer",),
            dash_table.DataTable(
                id='data-viewer',
                columns=[{'name': i, 'id':i, 'deletable':True, 'selectable':False} for i in main_dataframe.columns],
                data=main_dataframe.to_dict('records'),
                virtualization=True,
                filter_action='native',
                fixed_rows={'headers': True},
                style_cell={'minWidth': 70, 'width': 100, 'maxWidth': 140},
                style_table={'height': 400},
            )
        ])
    return data_viewer

# import pages.data_import1
# data_viewer = viewer_table(pages.data_import1.main_dataframe)

layout = dbc.Container([
    dcc.Store(id='filtering-query',storage_type='local'),
    dbc.Row([
        dbc.Col(
            html.H1("국민건강영양조사 분석 대시보드",
                className='text-center text-primary, mb-4',
                style = {"margin-top":"10px"}
            ), # mb-4 -> some padding
        width=12),
    ]),
    # data_viewer,
    dbc.Row(
        dbc.Col(dbc.Button(id="next-page1", color="dark", outline=True, n_clicks=0, children="Next", className="mt-4 px-0 py-0 mb-2 justify-content-end"),width={'size':1,'offset':3}), 
        justify="end",
    )
])


# @callback(
#     Output(component_id='filtering-query', component_property='data'),
#     # Input(component_id='next-page', component_property='n_clicks'),
#     Input(component_id='next-page1', component_property='filter_query'),
#     Input(component_id='item-3', component_property='n_clicks'),
# )
@callback(
    Output(component_id='filtering-query', component_property='data'),
    Input(component_id='next-page1', component_property='n_clicks'),
)
def check(n_clicks):
    print(n_clicks)
    return no_update