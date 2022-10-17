from mimetypes import init
from turtle import pd
import pandas as pd
import plotly
import plotly.express as px
import os

# path = ""
# os.listdir(path)
# data = pd.read_csv(path)

# class graphics(data):
#     def __init__(self, graph_type, variables_row, variables_col):
#         self.graph_type = ["histogram", "scatter", "line_plot", "box_plot"]
#         self.variables_col = []
#         self.variables_row = []

class graph:
    def __init__(self, graph_type, variables_row, variables_col):
        self.graph_type = graph_type
        self.variables_row = variables_row
        self.variables_col = variables_col
    
    def getGraph(graph_type, vairables_row, variables_col):
        if graph_type == 'box plot':
            pass
        elif graph_type == 'scatter':
            fig =px.scatter(x=range(10), y=range(10))
            fig.write_html("./file.html")
            return fig
        elif graph_type == 'line plot':
            pass
        elif graph_type == 'histogram':
            pass
            
        

