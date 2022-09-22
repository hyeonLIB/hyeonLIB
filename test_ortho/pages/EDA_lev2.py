import dash
# Import necessary libraries 
from dash_extensions.enrich import DashProxy
from dash import html
import dash_bootstrap_components as dbc
from tools import load_data, properties_specification
from dash import no_update, callback
from dash_extensions.enrich import dcc, html, dash_table, Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import os

# dash.register_page(__name__, path='/EDA_lev2')