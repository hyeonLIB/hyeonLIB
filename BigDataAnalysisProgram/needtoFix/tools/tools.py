import plotly.express as px
import pandas as pd
import numpy as np
import os
import io

"""
Tools for backside of frontend file
"""

"""Data load methods"""

# def load_data(file_name, data_path, format, to_csv=False, cmd_visiable=False):
#     if format == 'sas':
#         file_name = file_name.replace('.sas7bdat','')
#         df = pd.read_sas(f'{data_path}/{file_name}.sas7bdat', encoding='iso-8859-1', format='sas7bdat')
    

#     if cmd_visiable:
#         print(file_name)
#         print("data loaded successfully")
#         print("*** print 5 rows of data ***\n")
#         print(df.head())
#         print("*** column list ***\n")
        
#     if to_csv==True:
#         df.to_csv(f'{data_path}/csv/{file_name}.csv', index=False)
#         print("data has been saved to csv in csv directory")
    
#     return df

"""Data load methods"""

def load_data(file_name,data_path, to_csv=False):
    print(file_name)
    file_name = file_name.replace('.sas7bdat','')
    df = pd.read_sas(f'{data_path}/{file_name}.sas7bdat', encoding='iso-8859-1', format='sas7bdat')	
    df = df.rename(columns=str.lower)
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
    
def KNHANESPreprocessing(df):
    var_blu = ['HE_glu', 'HE_chol', 'HE_HDL_st2', 'HE_TG', 'HE_ast', 'HE_alt', 'HE_HB', 'HE_HCT', 'HE_BUN', 'HE_crea', 'HE_WBC', 'HE_RBC', 'HE_Bplt']
    var_uph = ['HE_Uph', 'HE_Unitr', 'HE_Usg', 'HE_Upro', 'HE_Uglu', 'HE_Uket', 'HE_Ubil', 'HE_Ubld', 'HE_Uro', 'HE_UNa']
    cat_var_ls = ['year','region','town_t','sex','apt_t','incm','ho_incm','edu','occp','sm_presnt','dr_month','pa_high','pa_mid','pa_walk',
                'DX_OST','DX_OST_TF','DX_OST_FN','DX_OST_LS'] + var_blu + var_uph # 범주형 변수(정수형)
    num_var_ls = ['age', 'HE_ht', 'HE_wt', 'HE_BMI', 'HE_wc',
                'DX_F_Ts_A','DX_S_Ts_A','DX_FN_Ts_A',
                'NF_INTK','NF_EN','NF_WATER','NF_PROT','NF_FAT','NF_CHO','NF_FIBER','NF_ASH',
                'NF_CA','NF_PHOS','NF_FE','NF_NA','NF_K','NF_VA','NF_CAROT','NF_RETIN','NF_B1','NF_B2','NF_NIAC','NF_VITC'] # 연속형 변수

    for v in cat_var_ls:
        df.loc[:,v]=pd.Categorical(df.loc[:,v].astype('int')) # 결측 등이 포함된 경우 errors='ignore' 추가

    for v in num_var_ls:
        df.loc[:,v]=df.loc[:,v].astype('float')

    # 연령 구분, 10세별 구분
    #pandas cut 함수를 이용할 수 있으나 70이상의 표현이 번거로울 수 있음
    #labels = ["{0} - {1}".format(i, i + 10) if i < 70 else " 70 +" for i in range(10, dt_dxa1['age'].max()+1, 10)]
    #dt_dxa1['age_10'] = pd.cut(dt_dxa1.age, range(10, dt_dxa1['age'].max()+11, 10), right=False, labels=labels, ordered=False)
    df.loc[:,'age_10'] = None
    df.loc[df['age'].between(10,  29, inclusive=True), 'age_10'] = 0
    df.loc[df['age'].between(30,  39, inclusive=True), 'age_10'] = 1
    df.loc[df['age'].between(40,  49, inclusive=True), 'age_10'] = 2
    df.loc[df['age'].between(50,  59, inclusive=True), 'age_10'] = 3
    df.loc[df['age'].between(60,  69, inclusive=True), 'age_10'] = 4
    df.loc[df['age'].between(70,  110, inclusive=True), 'age_10'] = 5
    df.loc[:,'age_10'] = pd.Categorical(df.loc[:,'age_10'])

    return df

def merge_DXA(main_dataframe, data_path): ## need to be class(merge function)
    main_dataframe = main_dataframe.astype({'year':'int32'}).astype({'year':'str'})
    year_list = list(main_dataframe['year'].unique())
    print(year_list)
    dir_list = os.listdir(data_path)
    
    # dxa  파일 연도 따라 유무 확인
    merged_dataframe = pd.DataFrame()
    dxa_dataframe = pd.DataFrame()
    
    for year in year_list:
        # year = year.replace("20","")
        year = year[2:]
        print(year)
        for file_name in dir_list:
            if year in file_name:
                print(file_name)
                file_path = data_path + '/' + file_name
                dxa = pd.read_sas(file_path, encoding='iso-8859-1', format='sas7bdat')
                print(dxa.columns)
                if 'ID' in dxa.columns:
                    dxa.rename(columns = {'ID':'id'}, inplace = True)
                dxa_dataframe = pd.concat([dxa_dataframe, dxa], ignore_index=True)

    merged_dataframe = main_dataframe.merge(dxa_dataframe,on='id', suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')

    return merged_dataframe


# main_dataframe = []
# global data_path
# data_path = '../raw_data'
# dir_list = os.listdir(data_path)
# dir_list.sort()