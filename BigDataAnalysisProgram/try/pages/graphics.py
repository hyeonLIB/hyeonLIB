# from pages import data_import

# layout = []

import dash
from dash import html

# dash.register_page(__name__)

from pages.analysis import hello
# data = hello
data=0
layout = html.Div(children=[
    html.H1(children=data),
])