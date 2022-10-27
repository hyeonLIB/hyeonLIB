from pages import data_import
from pages import data_import
import dash
from dash_extensions.enrich import dcc, html, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
from dash import no_update, callback
import plotly.express as px
import pandas as pd
import numpy as np

layout = dbc.Container([
    # html.Container([
    #     html.Container()
    # ])
    html.Div(id='tab', children='BigDataAnalysis'),
    dcc.Store(id='local',storage_type='local'),
    dcc.Store(id='local2',storage_type='local'),
    # dbc.Container([])
    html.H6(children="Data Selection",
    className='text-center',),
])