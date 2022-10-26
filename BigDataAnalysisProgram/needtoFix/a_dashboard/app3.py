import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from statsmodels.formula.api import ols
#from statsmodels.stats.anova import anova_lm

global result


df = pd.read_json('./Dataset_KNHANES_dxa_adj.json')
# 데이터 전처리
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

df = KNHANESPreprocessing(df)



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("SAT", className="display-4"),
        html.Hr(),
        html.P(
            "Simplified Analysis Tool", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Dataset viewer", href="/", active="exact"),
                dbc.NavLink("Step 1", href="/page-1", active="exact"),
                dbc.NavLink("Step 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)

def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1('The Korea National Health and Nutrition Examination Survey(KNHANES)',
                        style={'textAlign':'center'}),
                dash_table.DataTable(
                    columns=[
                        {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
                    ],
                    data=df.to_dict('records'),
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    #row_selectable="multi",
                    #row_deletable=True,
                    selected_columns=[],
                    #selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 10,
                )
                ]
    elif pathname == "/page-1":
        result = genTable1(df, var_tab1_col, var_tab1_row, percent_type='row').reset_index()
        return [
                html.H1('Table1',
                        style={'textAlign':'center'}),
                dash_table.DataTable(
                    columns=[
                        {"name": i, "id": i, "deletable": True, "selectable": True} for i in result.columns
                    ],
                    data=result.to_dict('records'),
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    #row_selectable="multi",
                    #row_deletable=True,
                    selected_columns=[],
                    #selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    #page_size= 7,
                )
                ]
    elif pathname == "/page-2":
        return [
                html.H1('Graph',
                        style={'textAlign':'center'}),
                dcc.Dropdown(
                    id='dropdown',
                    options=var_tab1_row,
                    value='sex',
                    clearable=False,
                ),
                dcc.Graph(id='graph',
                         #figure=fig
                        )
                ]

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(
            Output("graph", "figure"), 
            Input("dropdown", "value")
            )
def update_bar_chart(col_nm):
    result = genTable1(df, var_tab1_col, var_tab1_row, percent_type='row') #상속이 안되서 다시 재실행
    result_melt = pd.melt(result, value_name='values', ignore_index=False)
    result_melt = result_melt.reset_index()
    result_pvalue = result_melt.loc[result_melt['variable'] == 'p-value']
    pvalue = result_pvalue[result_pvalue['level_0']==col_nm]['values'].iloc[0]
    # Dropdown에서 입력 받은 value를 이용
    result_plt = result_melt.loc[(result_melt['level_0'] == col_nm) & (result_melt['variable'].str.contains("p")) & (result_melt['variable'] != 'p-value')]
    fig = px.bar(result_plt, x='variable', y='values', color='level_1', barmode='group',
                labels={"variable":'Osteoporosis level',"level_1": col_nm}
                ,title=f"p-value: {pvalue}"
                )
    return fig



##################################################################
var_tab1_row = ['sex', 'age', 'age_10','ho_incm','edu','occp', 'HE_BMI', 'HE_wc']
var_tab1_col = 'DX_OST'

from scipy.stats import chi2_contingency
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

def genTable1(in_dt, col_var, row_ls, percent_type='row'):
    tab = pd.DataFrame()
    for r in row_ls:
        if in_dt[r].dtype.name == 'category':
            tmp1 = pd.crosstab(columns=in_dt[col_var], index=in_dt[r]) # aggfunc를 선언하지 않으면 count
            uniColumns = [(tmp1.columns.name + str(c) + 'N') for c in tmp1.columns.values]
            tmp1.columns = uniColumns
            mulIndex = pd.MultiIndex.from_tuples([(r, c) for c in tmp1.index])
            tmp1 = tmp1.set_index(mulIndex)

            tmp2 = round(pd.crosstab(columns=in_dt[col_var], index=in_dt[r], normalize='columns')*100, 1) #columns
            uniColumns = [(tmp2.columns.name + str(c) + 'p') for c in tmp2.columns.values]
            tmp2.columns = uniColumns
            mulIndex = pd.MultiIndex.from_tuples([(r, c) for c in tmp2.index])
            tmp2 = tmp2.set_index(mulIndex)
            tmp3 = pd.concat([tmp1, tmp2], axis=1)
            tmp3.loc[tmp3.index[0], 'p-value'] = format(chi2_contingency(tmp1)[1], ".3f") # chisquared test: scipy의 chi2_contingency 이용, 독립성에 대한 카이제곱검정
            tab = pd.concat([tab, tmp3], axis=0).reindex(sorted(tmp3.columns), axis=1)
        else:
            tmp1 = round(pd.pivot_table(in_dt, columns=col_var, values=r , aggfunc=np.mean), 1)
            uniColumns = [(tmp1.columns.name + str(c) + 'N') for c in tmp1.columns.values]
            tmp1.columns = uniColumns
            mulIndex = pd.MultiIndex.from_tuples([(r, 'mean, std')])
            tmp1 = tmp1.set_index(mulIndex)
            tmp2 = round(pd.pivot_table(in_dt, columns=col_var, values=r , aggfunc=np.std), 1) #np.std : n-1
            uniColumns = [(tmp2.columns.name + str(c) + 'p') for c in tmp2.columns.values]
            tmp2.columns = uniColumns
            mulIndex = pd.MultiIndex.from_tuples([(r, 'mean, std')])
            tmp2 = tmp2.set_index(mulIndex)
            tmp3 = pd.concat([tmp1, tmp2], axis=1)
            model = ols(r+'~' + 'C('+col_var+')', data=in_dt).fit() # anova test
            tmp3.loc[tmp3.index[0], 'p-value'] = format(model.f_pvalue, ".3f")
            if tab.shape[0] > 0:
                tab = pd.concat([tab, tmp3], axis=0)
            else:
                tab = pd.concat([tab, tmp3], axis=0).reindex(sorted(tmp3.columns), axis=1)   
    tab.fillna('', inplace=True)
    return tab

if __name__ == '__main__':
	app.run_server(debug=True)