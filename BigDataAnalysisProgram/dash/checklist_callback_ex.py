# -*- coding: utf-8 -*-
from dash import Dash, dcc, html, Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

all_options = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': [u'Montréal', 'Toronto', 'Ottawa']
}
app.layout = html.Div([
    dcc.RadioItems(
        list(all_options.keys()),
        'America',
        id='countries-radio',
    ),

    html.Hr(),

    dcc.RadioItems(id='cities-radio'),

    html.Hr(),

    html.Div(id='display-selected-values')
])


@app.callback(
    Output('cities-radio', 'options'),
    Input('countries-radio', 'value'))
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]


@app.callback(
    Output('cities-radio', 'value'),
    Input('cities-radio', 'options'))
def set_cities_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    Input('countries-radio', 'value'),
    Input('cities-radio', 'value'))
def set_display_children(selected_country, selected_city):
    return u'{} is a city in {}'.format(
        selected_city, selected_country,
    )


if __name__ == '__main__':
    app.run_server(debug=True)




# # -*- coding: utf-8 -*-
# from dash import Dash, dcc, html
# from dash.dependencies import Input, Output, State
# import dash_design_kit as ddk

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = Dash(__name__, external_stylesheets=external_stylesheets)

# app.layout = html.Div([
#     dcc.Input(id='input-1-state', type='text', value='Montréal'),
#     dcc.Input(id='input-2-state', type='text', value='Canada'),
#     html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
#     html.Div(id='output-state')
# ])


# @app.callback(Output('output-state', 'children'),
#               Input('submit-button-state', 'n_clicks'),
#               State('input-1-state', 'value'),
#               State('input-2-state', 'value'))
# def update_output(n_clicks, input1, input2):
#     return u'''
#         The Button has been pressed {} times,
#         Input 1 is "{}",
#         and Input 2 is "{}"
#     '''.format(n_clicks, input1, input2)


# if __name__ == '__main__':
#     app.run_server(debug=True)    