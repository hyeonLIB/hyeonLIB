
import pandas as pd
import plotly.express as px

df = pd.read_csv('avocado-updated-2020.csv')

df.info()

print(df['type'].value_counts(dropna=False))
print(df['geography'].value_counts(dropna=False))


msk = df['geography'] == 'Los Angeles'

px.line(df[msk], x='date', y='average_price', color='type')


from dash import Dash, html, dcc, Input, Output
import plotly.express as px

avocado = pd.read_csv('avocado-updated-2020.csv')

app = Dash()

geo_dropdown = dcc.Dropdown(options=avocado['geography'].unique(),
                            value='New York')

app.layout = html.Div(children = [
    html.H1(children='Avocado Prices Dashboard'),
    geo_dropdown,
    dcc.Graph(id='price-graph')
])

@app.callback(
    Output(component_id='price-graph', component_property='figure'),
    Input(component_id=geo_dropdown, component_property='value')
)

def update_graph(selected_geography):
    filtered_avocado = avocado[avocado['geography'] == selected_geography]
    line_fig = px.line(filtered_avocado,
                        x='date', y='average_price',
                        color='type',
                        title=f'Avocado Prices in {selected_geography}')
    
    return line_fig


if __name__ == '__main__':
    app.run_server(debug=True)