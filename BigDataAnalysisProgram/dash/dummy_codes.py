# import plotly
# import plotly.graph_objs as go
# import plotly.plotly as py

# import numpy as np

# colorscale = [[0, '#FAEE1C'], [0.33, '#F3448E'], [0.66, '#9C1DE7'], [1, '#581B98']]
# trace1 = go.Scatter(
#     y = np.random.randn(500),
#     mode = 'markers',
#     marker=dict(
#         size = 16,
#         color = np.random.randn(500),
#         colorscale=colorscale,
#         showscale=True
#     )
# )

# data = [trace1]
# url_1 = py.plot(data, filename='scatter-for-dashboard', auto_open=False)
# py.iplot(data, filename='scatter-for-dashboard')


"""data_viewer"""
# from dash import Dash, html
# import pandas as pd
# import pyreadstat

# df = pd.read_sas('hn16_all.sas7bdat', encoding='iso-8859-1', format='sas7bdat')

# def generate_table(dataframe, max_rows=10):
#     dataframe = dataframe.iloc[:,:]
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ])


# app = Dash(__name__)

# app.layout = html.Div([
#     html.H4(children='국민건강영양조사'),
#     generate_table(df)
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)

########33# 


# alert when you click the shell
# from dash import Dash, Input, Output, callback, dash_table
# import pandas as pd
# import dash_bootstrap_components as dbc

# # with all of the data it's too heavy for to load on web
# df = pd.read_sas('hn16_all.sas7bdat', encoding='iso-8859-1', format='sas7bdat')

# df_viewer = df.loc[:10, ~df.columns.str.contains("wt_")]


# app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# app.layout = dbc.Container([
#     dbc.Label('Click a cell in the table:'),
#     dash_table.DataTable(df_viewer.to_dict('records'),[{"name": i, "id": i} for i in df_viewer.columns], id='tbl'),
#     dbc.Alert(id='tbl_out'),
# ])


# @callback(Output('tbl_out', 'children'), Input('tbl', 'active_cell'))
# def update_graphs(active_cell):
#     return str(active_cell) if active_cell else "Click the table"

# if __name__ == "__main__":
#     app.run_server(debug=True)



##############

# from dash import Dash, dash_table
# import pandas as pd
# from collections import OrderedDict

# df = pd.read_sas('hn16_all.sas7bdat', encoding='iso-8859-1', format='sas7bdat')

# df_viewer = df.loc[:, ~df.columns.str.contains("wt_")]
# # df_viewer = df.loc[:10, ~df.columns.str.contains("wt_")]

# app = Dash(__name__)

# data = OrderedDict(
#     [
#         ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"]),
#         ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
#         ("Temperature", [1, -20, 3.512, 4, 10423, -441.2]),
#         ("Humidity", [10, 20, 30, 40, 50, 60]),
#         ("Pressure", [2, 10924, 3912, -10, 3591.2, 15]),
#     ]
# )

# df = pd.DataFrame(
#     OrderedDict([(name, col_data * 10) for (name, col_data) in data.items()])
# )

# app.layout = dash_table.DataTable(
#     data=df.to_dict('records'),
#     columns=[{'id': c, 'name': c} for c in df.columns],
#     page_size=20,  # we have less data in this example, so setting to 20
#     style_table={'height': '300px', 'overflowY': 'auto'}
# )

# if __name__ == '__main__':
#     app.run_server(debug=True)

