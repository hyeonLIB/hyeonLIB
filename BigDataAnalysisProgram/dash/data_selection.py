from dash import Dash, dcc, html
import pandas as pd
from collections import OrderedDict
import os
# import plotly

data_path = './raw_data'
dir_list = os.listdir(data_path)
dir_list.sort()
print(dir_list)


"""Data load methods"""

def load_data(file_name,data_path, to_csv=False):
    print(file_name)
    file_name = file_name.replace('.sas7bdat','')
    df = pd.read_sas(f'{data_path}/{file_name}.sas7bdat', encoding='iso-8859-1', format='sas7bdat')
    print("data loaded successfully")
    
    if to_csv==True:
        df.to_csv(f'{data_path}/csv/{file_name}.csv', index=False)
        print("data has been saved to csv in csv directory")

    print("*** print 5 rows of data ***\n")
    print(df.head())
    print("*** column list ***\n")
    # print(df.columns.tolist())
    
    return df


# from dash import Dash, dcc, html
# import plotly.express as px


# app = Dash(__name__)

# app.layout = html.Div([
#     dcc.Checklist(
#         id="checklist",
#         options=[{"label": file_name, "value": file_name} for file_name in dir_list],
#         labelStyle={'display': 'block'},
#         style={"height":200, "width":200, "overflow":"auto"}
#     )
# ])

# if __name__ == "__main__":
#     app.run_server(debug=True)



from dash import dcc, html, Dash
from dash.dependencies import Input, Output

app = Dash(__name__)

app.layout = html.Div(
    [
        dcc.Checklist(
            id="checklist",
            options=[{"label": file_name, "value": file_name} for file_name in dir_list],
            labelStyle={"display": "block"},
            style={"height":300, "width":300, "overflow":"auto"},
            value=[],
        ),
        # html.Button("load", id="load-button", n_clicks=0),
    ]
)


@app.callback(Output("checklist", "value"), Input("load-button", "n_clicks"))
def change_values(n_clicks):
    return ["SF"] if n_clicks > 0 else print("hi")


if __name__ == '__main__':
    app.run_server(debug=True)