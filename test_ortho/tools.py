import pandas as pd
import numpy as np
import plotly.express as px

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
    
    return df

def properties_specification(df_viewer, selected_column, type):
    total_data = len(df_viewer)
    missing_data_count = df_viewer.isnull().sum()
    responds_data_count = total_data - missing_data_count
    rate_missing_data_count = missing_data_count/total_data * 100

    if type == 'categorical':
        """
        Categorical
        Specification of property
        클래스
        클래스 수
        클래스별 개체 수
        전체 데이터 수
        관측 수
        결측 수
        결측 비
        """
        name_class = df_viewer[selected_column].unique()
        num_classes = df_viewer[selected_column].nunique()
        num_class = df_viewer[selected_column].value_counts()
        properties = {
            "total_data":total_data,
            "responds_data":responds_data_count[selected_column],
            "missing_data":missing_data_count[selected_column], 
            "missing_data_rate":rate_missing_data_count[selected_column],
            "num_class":num_class,
            "num_classes":num_classes,
            "name_class":name_class
        }
        print("categorical value")
    else:
        """
        Numerical
        Specification of property
        전체 데이터 수
        관측 수
        결측 수
        결측 비
        """
        properties = {
            "total_data":total_data,
            "responds_data":responds_data_count[selected_column],
            "missing_data":missing_data_count[selected_column], 
            "missing_data_rate":rate_missing_data_count[selected_column],
        }
        print("numberable value")
    
    return properties