import dash
from dash import State, no_update
import dash_bootstrap_components as dbc
from dash_extensions.enrich import MultiplexerTransform, DashProxy, dcc, html, Input, Output
from dash.dependencies import Input, Output

app = DashProxy(__name__, use_pages=True, prevent_initial_callbacks=True, transforms=[MultiplexerTransform()],external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True,
            meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}])    


global has_been_init
has_been_init = 0
# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "13rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Menu", className="display-4", style={'textAlign': 'center'}),
        html.Hr(),
        html.P(['의료 빅데이터', html.Br(), '분석 프로그램'],
            className="lead", style={'textAlign': 'center'}
        ),
        dbc.Nav(
            [
                dbc.NavLink("Data import", href="/", active="exact"),
                dbc.Collapse(
                    dbc.Card([
                        dbc.NavLink("Data Extraction", href="/data_import1", active="exact", className='collapse-nav-link'),
                        dbc.NavLink("Data Viewer", href="/data_import2", active="exact", className='collapse-nav-link'),
                    ]),
                    id="collapse-import",
                    is_open=False,
                ),
                dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
                dbc.NavLink("EDA", href="/EDA", active="exact"),
                dbc.Collapse(
                    dbc.Card([
                        dbc.NavLink("- 빈도", href="/EDA-frequency", active="exact", className='collapse-nav-link'),
                        dbc.NavLink("- 상관", href="/EDA-correlation", active="exact", className='collapse-nav-link'),
                        dbc.NavLink("- 이상값", href="/EDA-anomalies", active="exact", className='collapse-nav-link'),
                    ]),
                    id="collapse-eda",
                    is_open=False,
                ),
                dbc.NavLink("Graphics", href='/graphics', active="exact"),
                dbc.NavLink("Data export", href='/dataexport', active="exact"),
                dbc.NavLink("Analysis", href='/analysis', active="exact"),
                dbc.Collapse(
                    dbc.Card([
                        dbc.NavLink("- 기술통계", href="/analysis-descriptive", active="exact", className='collapse-nav-link'),
                        dbc.NavLink("- 평균 비교", href="/analysis-Ttest", active="exact", className='collapse-nav-link'),
                        dbc.NavLink("- 회귀 분석", href="/analysis-regression", active="exact", className='collapse-nav-link'),
                        dbc.NavLink("- 기계 학습", href="/analysis-ml", active="exact", className='collapse-nav-link'),
                    ]),
                    id="collapse-analysis",
                    is_open=False,
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id='init',storage_type='session'),
    sidebar,
    dbc.Col([
        dash.page_container
    ], style={"margin-left": "13rem","margin-right": "2rem","padding": "2rem 1rem"},)
])

# do I have to combine them?
@app.callback(
    Output(component_id="collapse-import", component_property="is_open"),
    Input(component_id="url", component_property="pathname"),
    State(component_id="collapse-import", component_property="is_open"),
)
def collapse_dashboard_import(pathname, is_open):
    if pathname== "/":
        return not is_open
    elif pathname == "/data_import1" or pathname == "/data_import2":
        return True
    else:
        return False
@app.callback(
    Output(component_id="collapse-eda", component_property="is_open"),
    Input(component_id="url", component_property="pathname"),
    State(component_id="collapse-eda", component_property="is_open"),
)
def collapse_dashboard_eda(pathname, is_open):
    if pathname== "/EDA":
        return not is_open
    elif pathname == "/EDA-frequency" or pathname == "/EDA-correlation" or pathname == "/EDA-anomalies":
        return True
    else:
        return False
@app.callback(
    Output(component_id="collapse-analysis", component_property="is_open"),
    Input(component_id="url", component_property="pathname"),
    State(component_id="collapse-analysis", component_property="is_open"),
)
def collapse_dashboard_analysis(pathname, is_open):
    if pathname== "/analysis":
        return not is_open
    elif pathname == "/analysis-descriptive" or pathname == "/analysis-Ttest" or pathname == "/analysis-regression" or pathname == "/analysis-ml":
        return True
    else:
        return False

if __name__=='__main__':
    app.run_server(debug=True, port=8050)