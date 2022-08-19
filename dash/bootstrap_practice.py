from pydoc import classname
from turtle import width
from dash import Dash, dcc, html, Output, Input, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime

# start = datetime.datetime(2020,1,1)
# end = datetime.datetime(2020,12,3)

# df = web.DataReader(['AMZN','GOOGL','FB','PFE','BNTX','MRNA'],
#                     'stooq', start=start, end=end)

# df = df.stack().reset_index()
# print(df[:15])

# df.to_csv("mystocks.csv", index=False)

df = pd.read_csv("mystocks.csv")
print(df[:15])

# df_viewer = pd.read_sas('hn16_all.sas7bdat', encoding='iso-8859-1', format='sas7bdat')

# df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
            meta_tags=[{'name': 'viewport',
                        'content': 'width=device-width, initial-scale=1.0'}]
            )

# Layout section: Bootstrap
# --------------------------------------------------------------

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1("Stock Market dashboard",
                    className='text-center text-primary, mb-4'), # mb-4 -> some padding
            width=12
            )
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='my-dpdn', multi=False, value="AMZN",
                        options = [{'label':x, 'value':x} for x in sorted(df['Symbols'].unique())]),
            dcc.Graph(id='line-fig', figure={})], 
            width = {'size':4}),

        dbc.Col(
            [
            dcc.Dropdown(id='my-dpdn2', multi=True, value=['PFE','BNTX'],
                        options=[{'label':x, 'value':x} for x in sorted(df['Symbols'].unique())]),
            dcc.Graph(id='line-fig2', figure={})
            ], 
            width = {'size':4}),  # 'offset':1, 'order':1 

        dbc.Col([dcc.Graph(id='line-fig3', figure={})],
            width = {'size':3})
    ]),
    dbc.Row([ 
        dbc.Col([ 
            html.P("select company Stock :",
                    style = {"textDecoration": "underline"}),
            dcc.Checklist(id='my-checklist', value=['FB','GOOGL','AMZN'],
                        options = [{'label':x, 'value':x} for x in sorted(df['Symbols'].unique())],
                        labelClassName = 'mr-5 text-success'),
            dcc.Graph(id='my-hist', figure={})
        ], width={'size':4})
    ])
    # dbc.Row([ 
    #     dash_table.DataTable(
    #         data=df_viewer.to_dict('records'),
    #         columns=[{'id': i, 'name': i} for i in df_viewer.columns],
    #         virtualization=True,
    #         fixed_rows={'headers': True},
    #         style_cell={'minWidth': 80, 'width': 80, 'maxWidth': 80},
    #         style_table={'height': 380}  # default is 500
    #     )
    # ])
], fluid=True)  # no_gutters=True # no space between columns , justify = 'start' # start, center, end, between, around


# Callback section: connecting the components
# ------------------------------------------------------------------------
@app.callback(
    Output('line-fig', 'figure'),
    Input('my-dpdn', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols']==stock_slctd]
    figln = px.line(dff, x='Date', y='High')
    return figln


# Line chart - multiple
@app.callback(
    Output('line-fig2', 'figure'),
    Input('my-dpdn2', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    figln2 = px.line(dff, x='Date', y='Open', color='Symbols')
    return figln2


# Histogram
@app.callback(
    Output('my-hist', 'figure'),
    Input('my-checklist', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    dff = dff[dff['Date']=='2020-12-03']
    fighist = px.histogram(dff, x='Symbols', y='Close')
    return fighist

if __name__ == '__main__':
    app.run_server(debug=True, port=3000)