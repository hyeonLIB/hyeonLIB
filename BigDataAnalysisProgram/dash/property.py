#%%
import pandas as pd

global data_path
data_path = './raw_data'
dir_list = os.listdir(data_path)
dir_list.sort()

df_viewer = pd.read_sas('hn19_all.sas7bdat', encoding='iso-8859-1', format='sas7bdat') ##
global col_property
col_property = df_viewer

df_viewer = df_viewer.loc[:, ~df_viewer.columns.str.contains("wt_")]
# df_viewer = df_viewer.loc[:15] # need to remove
#%%
print(col_property.loc[0,:])
# %%
# def
total_data = len(df_viewer)
missing_data_count = col_property.isnull().sum()
responds_data_count = total_data - missing_data_count
rate_missing_data_count = missing_data_count/total_data * 100

selected_column = 'ID'

# if type(df_viewer.loc[1,selected_column])==str:
#     properties = [
#         total_data,
#         responds_data_count[selected_column],
#         missing_data_count[selected_column], 
#         rate_missing_data_count[selected_column]
#     ]
#     print("categorical value")
# else:
#     properties = [
#         total_data,
#         responds_data_count[selected_column],
#         missing_data_count[selected_column], 
#         rate_missing_data_count[selected_column]
#     ]
#     print("numberable value")
# if type(df_viewer.loc[1,selected_column])==str:
#     properties = [
#         f"{total_data}",
#         f"{responds_data_count[selected_column]}",
#         f"{missing_data_count[selected_column]}", 
#         f"{rate_missing_data_count[selected_column]}%"
#     ]
#     print("categorical value")
# else:
#     properties = [
#         f"{total_data}",
#         f"{responds_data_count[selected_column]}",
#         f"{missing_data_count[selected_column]}", 
#         f"{rate_missing_data_count[selected_column]}%"
#     ]
#     print("numberable value")

def properties_specification(df_viewer, selected_column):
    total_data = len(df_viewer)
    missing_data_count = col_property.isnull().sum()
    responds_data_count = total_data - missing_data_count
    rate_missing_data_count = missing_data_count/total_data * 100

    if type(df_viewer.loc[1,selected_column])==str:
        properties = {
            "total_data":f"{total_data}",
            "responds_data":f"{responds_data_count[selected_column]}",
            "missing_data":f"{missing_data_count[selected_column]}", 
            "missing_data_rate":f"{rate_missing_data_count[selected_column]}%"
        }
        print("categorical value")
    else:
        properties = {
            "total_data":f"{total_data}",
            "responds_data":f"{responds_data_count[selected_column]}",
            "missing_data":f"{missing_data_count[selected_column]}", 
            "missing_data_rate":f"{rate_missing_data_count[selected_column]}%"
        }
        print("numberable value")
    
    return properties
properties = properties_specification(df_viewer, selected_column)
print(properties)
# %%
print(len(col_property))
# %%
type(df_viewer.loc[1,'town_t'])

# %%
pr = df_viewer.loc[1,:]
print(type(pr))
t_list=[]
for i in pr:
    t_list.append(type(i))

t_list = set(t_list)
# %%
print(t_list)
# %%
