from dash_extensions.enrich import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px

def major_class_checklist(major_classes):
    '''
    major class component
    checklist
    '''
    return dcc.Checklist(
        id = 'checklist-major',
        options = [{'label':major_class,'value':major_class} for major_class in major_classes],
        labelStyle={'display':'block'},
        style = {'height':300, 'width':300, 'overflow':'auto', 'fontSize':20},
        labelClassName = 'pb-3',
        value = [],
    )


def minor_class_checklist(minor_classes):
    '''
    subclass component
    checklist or table
    '''
    return dcc.Checklist(
        id = 'checklist-minor',
        options = [{'label':minor_class,'value':minor_class} for minor_class in minor_classes],
        labelStyle={'display':'block'},
        style = {'height':300, 'width':300, 'overflow':'auto', 'fontSize':20},
        labelClassName = 'pb-3',
        value = [],
    )

def year_selection_checklist(year_list):
    '''
    select year component
    checklist
    '''
    return dcc.Checklist(
        id = 'checklist-year',
        options = [{'label':year,'value':year} for year in year_list],
        labelStyle={'display':'block'},
        style = {'height':300, 'width':300, 'overflow':'auto', 'fontSize':20},
        labelClassName = 'pb-3',
        value = [],
    )

def select_variable_table(dataframe):
    '''
    select variable component
    table with activation function - modal
    circular sycronize with selected variable component
    '''
    return dash_table.DataTable(
                id='table-col-selection',
                columns=[{'name':'col_name','id':'col_name'},{'name':'col_type','id':'col_type'}],
                data=[
                    {'col_name':i, 'col_type':'numeric'}
                    if 'float' in str(type(dataframe.iloc[1][i]))
                    else {'col_name':i,'col_type':'categorical'
                    } for i in dataframe.columns
                ],
                virtualization=True,
                row_selectable='multi',
                selected_rows=[],
                fixed_rows={'headers': True},
                style_cell={'font_size':'24px','minWidth': 70, 'width': 100, 'maxWidth': 140, 'padding-right': '30px'},
                style_data={'whiteSpace':'normal', 'height':'auto'},
                style_table={'margin-bottom':'15px'},
                style_cell_conditional=[
                    {'if': {'column_id': i},
                        'textAlign': 'left',
                        'padding-left' : '20px', 
                    } for i in ['col_name']
                ],
                style_as_list_view=True,
                page_action='none',
            ),

def selected_variable_checklist():
    '''
    selected variable component
    checklist(removable)
    circular syncronize with select variable component
    '''
    return html.Div([
        dcc.Checklist(
            id = 'checklist-col-selected',
            options = [],
            labelStyle={'display':'block'},
            style = {'margin':'25px','overflow':'auto','height':460, 'fontSize':22},
            labelClassName = 'pb-3',
            value = [],
        )
        ], style={'height':500, 'border':'3px grey solid', 'border-radius': '10px'}
    )

def property_specification_modal():
    '''
    property specification modal component
    modal
    '''
    return dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("변수 속성 명세서"), close_button=True),
        dbc.ModalBody([
            dbc.Row("Initialize"),
            dbc.Row([
                dbc.Col(
                    [dbc.Button(
                        "변수 타입 변경",
                        id="change-col-type",
                        className="ms-auto px-0 py-0 mb-2",
                        n_clicks=0,
                    )]
                )
            ],),
        ],),
        dbc.ModalFooter(
            dbc.Button(
                "Close",
                id="close-properties-specification",
                className="ms-auto",
                n_clicks=0,
            ),
        ),],
        id="modal-properties-specification",
        is_open=False,
        scrollable=True,
        size="lg",
        backdrop=True,
        fade=True,
        centered=True,
    )
    
def properties_specification_component(main_dataframe, col_property_info, selected_column, col_type):
    if col_type == "categorical":
        total =         f"  전   체 : {col_property_info['total_data']} "
        responds=       f"  응답수 : {col_property_info['responds_data']} "
        missing=        f"  결측수 : {col_property_info['missing_data']} "
        missing_rate =  f"  결측비 : {round(col_property_info['missing_data_rate'],2)} "
        
        # column propert viewer dataframe -> datatable
        column_property_viewer = [
            {'name':'index','id':'index'},
            {'name':'code_class','id':'code_class'},
            {'name':'name_class','id':'name_class'},
            {'name':'num_class','id':'num_class'},
            {'name':'ratio_class','id':'ratio_class'},
        ]
        """index, name_class, name_class, num_class, num_class/len(total)"""
        data_property_viewer = [
            {'index':i,
            'code_class':col_property_info['name_class'][i],
            'name_class':col_property_info['name_class'][i],
            'num_class':col_property_info['num_class'][i],
            'ratio_class':round(col_property_info['num_class'][i]/col_property_info['total_data'],4)
            } for i in range(col_property_info['num_classes'])
        ]
        
        # Modal component for Variable property sepecification
        modal_children = [
            dbc.ModalHeader(dbc.ModalTitle(f"{selected_column} 속성 명세서 - {col_type}"), close_button=True),
            dbc.ModalBody(
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "변수 타입 변경",
                                id="change-col-type",
                                className="ms-auto px-0 py-0 mb-2",
                                n_clicks=0,
                            ),
                        ],),
                    ],),
                    dbc.Row([
                        dbc.Col(
                            dbc.CardGroup([
                                dash_table.DataTable(
                                    columns = column_property_viewer,
                                    data=data_property_viewer,
                                    virtualization=True,
                                    fixed_rows={'headers': True},
                                    style_as_list_view=True,
                                    style_cell={'minWidth': 50,'width': 110},
                                    style_cell_conditional=[
                                        {
                                            'if': {'column_id': i},
                                            'textAlign': 'center',
                                            'width': 50
                                        } for i in ['index']
                                    ],
                                ),
                            ],), width=6
                        ),

                        dbc.Col([
                            dbc.ListGroup([
                                dbc.ListGroupItem(total),
                                dbc.ListGroupItem(responds),
                                dbc.ListGroupItem(missing),
                                dbc.ListGroupItem(missing_rate),
                            ]),
                        ], width=2,),

                        dbc.Col([
                            html.Div(
                                style={'width': '135%', 'display':'inline-block', 'outline':'thin lightgrey solid'},
                                children=[
                                    dcc.Graph(
                                        id = {'type':'class-graph'},
                                        figure=px.pie(main_dataframe, names = selected_column, title=selected_column)
                                    ),
                                ]
                            ),
                        ], width=4,),                    
                    ],),
                ],),
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Close",
                    id="close-properties-specification",
                    className="ms-auto",
                    n_clicks=0,
                ),
            ),
        ]

    elif col_type == "numeric":
        total =         f" 전   체 : {col_property_info['total_data']} "
        responds=       f" 응답수 : {col_property_info['responds_data']} "
        missing=        f" 결측수 : {col_property_info['missing_data']} "
        missing_rate =  f" 결측비 : {round(col_property_info['missing_data_rate'],2)} "

        # Modal component for Variable property sepecification 
        modal_children = [
            dbc.ModalHeader(dbc.ModalTitle(f"{selected_column} 속성 명세서 - {col_type}"), close_button=True),
            dbc.ModalBody(
                dbc.Form([
                    dbc.Row([
                        dbc.Col(
                            dbc.Button(
                                "변수 타입 변경",
                                id="change-col-type",
                                className="ms-auto px-0 py-0 mb-2",
                                n_clicks=0,
                            ),
                        ),
                    ],),
                    dbc.Row([    
                        dbc.Col(
                            dbc.ListGroup([
                                dbc.ListGroupItem(total),
                                dbc.ListGroupItem(responds),
                                dbc.ListGroupItem(missing),
                                dbc.ListGroupItem(missing_rate),
                            ],), width=4
                        ),

                        dbc.Col([
                            html.Div(
                                style={'width': '135%', 'display':'inline-block', 'outline':'thin lightgrey solid'},
                                children=[
                                    dcc.Graph(
                                        id = {'type':'class-graph'},
                                        figure=px.histogram(main_dataframe, x=selected_column, color="sex",
                                                            marginal="box", title=selected_column) # or violin, rug
                                    ),
                                ]
                            ),
                        ], width=4,),
                    ],),
                ],),
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Close",
                    id="close-properties-specification",
                    className="ms-auto",
                    n_clicks=0,
                ),
            ),
        ]

    return modal_children  