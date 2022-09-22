import dash
from dash_extensions.enrich import MultiplexerTransform, DashProxy
import dash_bootstrap_components as dbc
from dash import html, dcc

"""
transforms=[MultiplexerTransform()]
    - Was problem : Default -> A component can have output from only ONE other component
    - Solved by using above method
prevent_initial_callbacks=True
    - For the speed of load data have been initialized
    - It prevents callback functions are activated while on processing classes of component on the app layout are instantiated.
"""

# Application
# -------------------------------------------------------------

app = DashProxy(__name__, use_pages=True, prevent_initial_callbacks=True, transforms=[MultiplexerTransform()],external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}])

app.layout = dbc.Container([
    html.Div("빅데이터 분석 대시보드", id='head', style={'fontSize':50, 'textAlign':'center'}),
    html.Hr(),

    dash.page_container
])

if __name__ == "__main__":
    app.run(debug=True) 
