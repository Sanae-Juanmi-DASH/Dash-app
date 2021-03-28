
#Loading libraries:
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table as dt
import pandas as pd
import plotly.express as px
import json
import numpy as np
import plotly.graph_objects as go

external_stylesheets = [dbc.themes.SOLAR]

#Creating app:
app = dash.Dash(__name__, title="Dash App",external_stylesheets=external_stylesheets)


#Loading dataset "House Prices":
col_names_hp=["price","lotsize","bedrooms","bathrooms","stories","driveway","recreation","fullbase","gasheat","aircon","garage","prefer"] 
hp_data= pd.read_csv('ag-data.fil', sep="\s+", names=col_names_hp)
hp_cols = [{"name": i, "id": i} for i in hp_data.columns]

#Data tyding house prices:
categ_cols_hp=["bedrooms","bathrooms","stories","driveway","recreation","fullbase","gasheat","aircon","garage","prefer"] 
for col in categ_cols_hp:
    hp_data[col]= hp_data[col].map(int)
    hp_data[col]= hp_data[col].astype(object)


#Checklist House prices:
checklist_hp=html.Div([
    html.Br(),
    html.H4('House Prices Data table'),
    html.Br(),
    html.H5('Filters'),
    dcc.Checklist(id="hp-checklist",
    options=[
        {'label': 'No garage', 'value': 'garage'},
        {'label': 'No air conditioning', 'value': 'aircon'}
       
    ],
    labelStyle = dict(display='block')
),
html.Br()
])


#House prices table:
table_hp = html.Div([
    dt.DataTable(id="hp-table",
        columns = hp_cols,
        data= hp_data.to_dict("records"),
        fixed_rows={'headers': True},
        sort_action="native",
        sort_mode='multi',
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_header={'backgroundColor': 'rgb(11, 65, 86)'},
        style_cell={
            'backgroundColor': 'rgb(106, 146, 162)',
            'color': 'white'
        },
             
    ),
     html.Br()
])

html.Br()

# Loading dataset "diabetes"
diabetes = pd.read_csv('diabetes.csv',sep=',')
col_diabetes = [{"name": i, "id": i} for i in diabetes.columns]


#diabetes  table:
table_diabetes = html.Div([
    dt.DataTable(id="diabetes-table",
        columns = col_diabetes,
        data= diabetes.to_dict("records"),
        fixed_rows={'headers': True},
        sort_action="native",
        sort_mode='multi',
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_header={'backgroundColor': 'rgb(11, 65, 86)'},
        style_cell={
            'backgroundColor': 'rgb(106, 146, 162)',
            'color': 'white'
        },
             
    ),
     html.Br()
])

#Checklist Dibetes:
checklist_diabetes=html.Div([
    html.Br(),
    html.H4('Diabetes Data table'),
    html.Br(),
    html.H5('Filters'),
    dcc.Checklist(id="diabetes-checklist",
    options=[
        {'label': 'Diabetes', 'value': '1'},
        {'label': 'No Diabetes', 'value': '0'}
       
    ],
    labelStyle = dict(display='block')
),
html.Br()
])


#Dropdown plots:
fig_names=["Histogram", "Scatter", "Boxplot"]
dropdown_plot=html.Div([
        html.Br(),
        html.H4('Dynamic Plots'),
        html.Label(["Select the type of plot:",
            dcc.Dropdown(id='dropdown-plots',
                options= [{'label': x, 'value': x} for x in fig_names],
                value= "Histogram",
                multi= False,
                style={"width": "100%"}
            )
            
        ]),
        html.Br()
            
])

#Dropdown plots diabetes:
dropdown_plot_diabetes=html.Div([
        html.Br(),
        html.H4('Dynamic Plots'),
        html.Br(),
        html.Label(["Select the type of plot:",
            dcc.Dropdown(id='dropdown-plots_diabetes',
                options= [{'label': i, 'value': i} for i in fig_names],
                value= "Histogram",
                multi= False,
                style={"width": "100%"}
            )
            
        ]),
        html.Br()
            
])

#Dropdown variables:
dropdown_vars=html.Div([
        html.Label(["Select a grouping variable:",
            dcc.Dropdown(id='dropdown-vars',
                options= [{'label': x, 'value': x} for x in categ_cols_hp],
                value= "garage",
                multi= False,
                style={"width": "100%"}
            )
        ])
            
])

#Dropdown variables:
dropdown_vars_diabetes=html.Div([
        html.Label(["Select a variable:",
            dcc.Dropdown(id='dropdown-vars-diabetes',
                options= [{'label': i, 'value': i} for i in col_diabetes],
                value= "Pregnacies",
                multi= False,
                style={"width": "100%"}
            )
        ])
            
])


#User:
app.layout = html.Div([
    html.Div([
        html.H1(app.title, className= "app-header--title")]),
    dcc.Tabs(id="tabs-global", value='tab-1', children=[
        dcc.Tab(label='House prices', value='tab-1'),
        dcc.Tab(label='Diabetes', value='tab-2'),
    ], colors={
        "border": "white",
        "primary": "Linen",
        "background": "MediumAquaMarine"
    }),
    html.Div(id='tabs-single'),
    html.Div(id='plot_dp'),
    html.Div(id='slider'),
    html.Div(id="n_s", style= {'display': 'none'} )
])


#Update datatable:
@app.callback(
    Output('hp-table', 'data'),
    Input('hp-checklist', 'value')
)

def update_table(categ):
    if categ!=None:
        new_data=hp_data.loc[hp_data[categ[0]] == 0]      
        return new_data.to_dict("records")
    else:
        new_data=hp_data
        return new_data.to_dict("records")



#Update diabetes datatable:
@app.callback(
    Output('table-diabetes', 'data'), 
    Input('diabetes-checklist', 'value'))
def update_table2(value):
    if value==1:
        new_diabetes = diabetes[diabetes['Outcome'] == 1] 
        return new_diabetes.todict("records")

    elif value==0:
        new_diabetes = diabetes[diabetes['Outcome'] == 0] 
        return new_diabetes.todict("records")
    else:
        return table_diabetes


#Change content in selected tab:
@app.callback(
    Output('tabs-single', 'children'),
    Input('tabs-global', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            checklist_hp,
            table_hp,
            dropdown_plot,
            dropdown_vars
        ])
        
    elif tab == 'tab-2':
        return html.Div([
            checklist_diabetes,
            table_diabetes,
            dropdown_plot_diabetes,
            dropdown_vars_diabetes
        ])

#Change bins:
@app.callback(
    Output('n_s', 'children'),
    Input('hp-bins', 'value')
)
def binds (pric):
    return pric


#Change plot type:
@app.callback(
    Output('plot_dp', 'children'),
    Input('dropdown-plots', 'value'),
    Input('dropdown-vars','value'),
    Input('tabs-global', 'value'),
    Input('hp-table','data'),
    Input('n_s','children')
)
def render_plot(dp,vars,tab,table,pric):
    if tab=='tab-1':
            if  dp=='Scatter':
                return html.Div([
                    html.Br(),
                    html.P('Note that you can select points by clicking on the Lasso Select filter that appears on the top bar of the graph. Once the points are selected, the selected data will appear in the table below.'),
                    dcc.Graph(id="hp_scatter",
                    figure=px.scatter(table, x="price", y="lotsize", color=vars,custom_data=["price"])
                    ),
                    dt.DataTable(id="selected_data",
                        columns = hp_cols,
                        style_table={'height': '300px', 'overflowY': 'auto'},
                        style_header={'backgroundColor': 'rgb(11, 65, 86)'},
                        style_cell={
                            'backgroundColor': 'rgb(106, 146, 162)',
                            'color': 'white'
                        },
             
    )
                ])
            elif dp=='Histogram':
                return html.Div([
                    dcc.Graph(id="hp_hist",figure=px.histogram(table,x="price", color=vars, nbins=pric)),
                    html.P("Select the histogram bins:"),
                    dcc.Slider(id="hp-bins", min=0, max=40, value=pric, 
                    marks=
                    {
                        0: {'label': '0', 'style': {'color': '#77b0b1'}},
                        10: {'label': '10'},
                        20: {'label': '20'},
                        30: {'label': '30'},
                        40: {'label': '40', 'style': {'color': '#f50'}}
                    }
                    )
                    
                ])
            elif dp=='Boxplot':
                return html.Div([
                    dcc.Graph(id="hp_boxplot",figure=px.box(table,y="price", x=vars, color=vars,notched=True)
                )
])    

#Select data with lasso:
@app.callback(
    Output('selected_data', 'data'),
    Input('hp_scatter', 'selectedData'))
def display_selected_data(selectedData):
    if selectedData is None:
        return None
    prices= [i['customdata'][0] for i in selectedData['points']]
    filter=hp_data['price'].isin(prices)
    return hp_data[filter].to_dict("records")




if __name__ == '__main__':
    app.server.run(debug=True)