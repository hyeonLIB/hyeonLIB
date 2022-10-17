import sys
import json
import ast
import pandas as pd
import plotly.express as px
import os

input = ast.literal_eval(sys.argv[1])

global data_path
data_path = './raw_data'
dir_list = os.listdir(data_path)
dir_list.sort()

# Initialize dataframe
global df_viewer, main_dataframe

df_viewer = pd.read_sas(f'{data_path}/{dir_list[-1]}', encoding='iso-8859-1', format='sas7bdat')
df_viewer = df_viewer.rename(columns=str.lower)
main_dataframe = df_viewer
df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]
df_viewer = df_viewer.loc[:15] # need to remove

data_to_pass_back = 'Send this to node process'

x_columns = input['x_col']
y_columns = input['y_col']
graph_type = input['graph_type']

print(x_columns,y_columns,graph_type)

def drawGraph(x_columns, y_columns,graph_type):
    if graph_type == 'scatter':
        fig =px.scatter(x=df_viewer['sex'], y=df_viewer['age'])
        fig.write_html("./testfile.html")
        return fig
    elif graph_type == 'box plot':
        return graph_type
    elif graph_type == 'line plot':
        return graph_type
    elif graph_type == 'histogram':
        return graph_type

print("Generating px graph has been done")