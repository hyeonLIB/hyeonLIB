import dash
import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc, html, Input, Output, State, callback

dash.register_page(__name__, path='/')

category_list = ['국민건강영양조사','기타 데이터']

# Define the index page layout
layout = dbc.Container([
    # dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col(
            dcc.RadioItems(
                id="select-category",
                options=[{"label": category, "value": category} for category in category_list],
                labelStyle={"display": "block"},
                style={"height":300, "width":307, "overflow":"auto", "fontSize":18},
                labelClassName='pb-3',
                value='국민건강영양조사'
            ), width={"size": 6, "offset": 3},
        ),],
        id = 'select',
        align='center',
        justify='center',
    ),
    dbc.Row([
        dbc.Col(dbc.Button("선택",id='p',href='/EDA_lev1'),
        width={'size':6, 'offset':6},),
    ],
    id = 'category-button',
    align = 'center',
    justify='center',
    ),
    # html.Div(id='page-content', children=[]),
])

# @callback(
#     Output(component_id='select', component_property='children'),
#     Output(component_id='category-button', component_property='children'),
#     Output(component_id='page-content', component_property='children'),
#     Output(component_id='head', component_property='children'),
#     Input(component_id='url', component_property='pathname'),
#     State(component_id='select-category', component_property='value'),
#     # State(component_id='p', component_property='href')
# )

# def display_page(pathname, category):
#     if pathname == '/':
#         return no_update
#     if pathname == '/EDA_lev1':
#         row_content = [
#             dbc.Col(
#                 html.Div(),
#             )
#         ]
#         return row_content, row_content, EDA_lev1.layout, category+' 분석 대시보드'
#     if pathname == '/EDA_lev2':
#         return EDA_lev2.layout, category+' 분석 대시보드'
#     else:
#         return "404 Page Error! Please choose a link"