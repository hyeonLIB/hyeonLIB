# from flask import app
# import os
# os.chdir('../')
# import app
from dash_extensions.enrich import html

layout_not_initialized = [
                html.H1("HAS NOT BEEN INITIALIZED", className="text-danger"),
                html.Hr(),
                html.P(f"You cannot open this page before import data..."),
            ]

# layout_not_found = 