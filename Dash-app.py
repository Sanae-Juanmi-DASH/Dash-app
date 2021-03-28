
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

################################# PAGE DESIGN:


#Creating app:
app = dash.Dash(__name__, title="Dash App",external_stylesheets=external_stylesheets)

# the style arguments for the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# content page style:
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

#Main slide bar items:
sidebar = html.Div(
    [
        html.H2("Dash App", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("House prices dataset", href="/page-1", active="exact"),
                dbc.NavLink("Diabetes dataset", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

#Creating sidebar_style:
Sidebar_style= {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

################################# DATA MANIPULATION:

#####House prices:
#Loading dataset "House Prices":
col_names_hp=["price","lotsize","bedrooms","bathrooms","stories","driveway","recreation","fullbase","gasheat","aircon","garage","prefer"] 
hp_data= pd.read_csv('ag-data.fil', sep="\s+", names=col_names_hp)
hp_cols = [{"name": i, "id": i} for i in hp_data.columns]

#Data tyding house prices:
categ_cols_hp=["bedrooms","bathrooms","stories","driveway","recreation","fullbase","gasheat","aircon","garage","prefer"] 
for col in categ_cols_hp:
    hp_data[col]= hp_data[col].map(int)
    hp_data[col]= hp_data[col].astype(object)

#New column to identif rows:
idx = 0
new_col = hp_data.index + 1
hp_data.insert(loc=idx, column='ID', value=new_col)


#####Diabtes:
# Loading dataset "diabetes"
diabetes = pd.read_csv('diabetes2.csv',sep=',')
col_diabetes = [{"name": i, "id": i} for i in diabetes.columns]



################################# USER:

#####House prices:
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

#####Diabetes:

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






################################# SERVER:

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div([
            html.H1("Brief Introduction"),
            html.Br(),
            html.Br(),
            html.H2("House Prices Data Set"),
            html.Br(),
            html.H4("Context"),
            html.P("Sales prices of houses sold in the city of Windsor, Canada, during July, August and September, 1987."),
            html.P("The objective is to predict houses prices."),
            html.Br(),
            html.H4("Content"),
            html.P("A data frame containing 546 observations on 12 variables."),
            dcc.Markdown('''

            **- Price:** Sale price of a house.
            
            **- lotsize:** Lot size of a property in square feet.
            
            **- bedrooms:** Number of bedrooms.
            
            **- bathrooms:** Number of full bathrooms.
            
            **- stories:** Number of stories excluding basement.
            
            **- driveway:** Factor. Does the house have a driveway?
            
            **- recreation:** Factor. Does the house have a recreational room?
            
            **- fullbase:**Factor. Does the house have a full finished basement?

            **- gasheat:** Factor. Does the house use gas for hot water heating?
           
            **- aircon:** Factor. Is there central air conditioning?
           
            **- garage:** Number of garage places.
            
            **- gasheat:** Factor. Does the house use gas for hot water heating?
            
            **- prefer:** Factor. Is the house located in the preferred neighborhood of the city?

           
            #### Source
            
            Journal of Applied Econometrics Data Archive.

            [http://qed.econ.queensu.ca/jae/1996-v11.6/anglin-gencay/]


            #### References

            Anglin, P., and Gencay, R. (1996). Semiparametric Estimation of a Hedonic Price Function. Journal of Applied Econometrics, 11, 633–648.

            Verbeek, M. (2004). A Guide to Modern Econometrics, 2nd ed. Chichester, UK: John Wiley.
            '''),
            html.Br(),
            html.H2("Diabetes Data Set"),
            html.Br(),
            html.H4("Context"),
            html.P("This dataset is originally from the National Institute of Diabetes and Digestive and Kidney Diseases."),
            html.P("The objective is to predict based on diagnostic measurements whether a patient has diabetes."),
            html.Br(),
            html.H4("Content"),
            html.P("Several constraints were placed on the selection of these instances from a larger database."),
            html.P("In particular, all patients here are females at least 21 years old of Pima Indian heritage."),
            dcc.Markdown('''

            **- Pregnancies:** Number of times pregnant.
            
            **- Glucose:** Plasma glucose concentration a 2 hours in an oral glucose tolerance test.
            
            **- BloodPressure:** Diastolic blood pressure (mm Hg).
            
            **- SkinThickness:** Triceps skin fold thickness (mm)
            
            **- Insulin:** 2-Hour serum insulin (mu U/ml).
            
            **- BMI:** Body mass index (weight in kg/(height in m)^2).
            
            **- DiabetesPedigreeFunction:** Diabetes pedigree function.
            
            **-  Age:** Age (years).

            **-  Outcome:** Class variable (0 or 1).

            
            ''')
            

        ])
    elif pathname == "/page-1":
        return html.Div([
                html.Div([
                    html.H1(app.title, className= "app-header--title")]),
                dcc.Tabs(id="tabs-global-hp", value='tab-1-hp', children=[
                    dcc.Tab(label='Descriptive Analysis', value='tab-1-hp'),
                    dcc.Tab(label='Model prediction', value='tab-2-hp'),
                ], colors={
                    "border": "white",
                    "primary": "Linen",
                    "background": "MediumAquaMarine"
                }),
                html.Div(id='tabs-single-hp'),
                html.Div(id='plot-dp-hp'),
                html.Div(id='slider-hp'),
                html.Div(id="ns-hp", style= {'display': 'none'} )
            ])
                
                
    elif pathname == "/page-2":
        return html.Div([
                html.Div([
                    html.H1(app.title, className= "app-header--title")]),
                dcc.Tabs(id="tabs-global-d", value='tab-1-d', children=[
                    dcc.Tab(label='Descriptive Analysis', value='tab-1-d'),
                    dcc.Tab(label='Model prediction', value='tab-2-d'),
                ], colors={
                    "border": "white",
                    "primary": "Linen",
                    "background": "MediumAquaMarine"
                }),
                html.Div(id='tabs-single-d'),
                html.Div(id='plot-dp-d'),
                html.Div(id='slider-d'),
                html.Div(id="ns-d", style= {'display': 'none'} )
            ])
                
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


#Change content in selected tab:
@app.callback(
    Output('tabs-single-hp', 'children'),
    Input('tabs-global-hp', 'value')
)
def render_content(tab):
    if tab == 'tab-1-hp':
        return html.Div([
            checklist_hp,
            table_hp,
            dropdown_plot,
            dropdown_vars
        ])
        
    elif tab == 'tab-2-hp':
        return None


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


#Change bins:
@app.callback(
    Output('ns-hp', 'children'),
    Input('hp-bins', 'value')
)
def binds (pric):
    return pric


#Change plot type:
@app.callback(
    Output('plot-dp-hp', 'children'),
    Input('dropdown-plots', 'value'),
    Input('dropdown-vars','value'),
    Input('tabs-global-hp', 'value'),
    Input('hp-table','data'),
    Input('ns-hp','children')
)
def render_plot(dp,vars,tab,table,pric):
    if tab=='tab-1-hp':
            if  dp=='Scatter':
                return html.Div([
                    html.Br(),
                    html.P('Note that you can select points by clicking on the Lasso Select filter that appears on the top bar of the graph. Once the points are selected, the selected data will appear in the table below.'),
                    dcc.Graph(id="hp_scatter",
                    figure=px.scatter(table, x="price", y="lotsize", color=vars,custom_data=["ID"])
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
                    dcc.Graph(id="hp_boxplot",figure=px.box(table,y="price", x=vars, color=vars,notched=True,points="all",custom_data=["ID"])
                    ),
                    dt.DataTable(id="selected_points",
                        columns = hp_cols,
                        style_table={'height': '300px', 'overflowY': 'auto'},
                        style_header={'backgroundColor': 'rgb(11, 65, 86)'},
                        style_cell={
                            'backgroundColor': 'rgb(106, 146, 162)',
                            'color': 'white'
                        },
             
    )
                
])    

#Select data with lasso scatterplot:
@app.callback(
    Output('selected_data', 'data'),
    Input('hp_scatter', 'selectedData'))
def display_selected_data(selectedData):
    if selectedData is None:
        return None
    prices= [i['customdata'][0] for i in selectedData['points']]
    filter=hp_data['ID'].isin(prices)
    return hp_data[filter].to_dict("records")

#Select data with boxplots:
@app.callback(
    Output('selected_points', 'data'),
    Input('hp_boxplot', 'clickData'))
def display_sele_data(click):
    if click is None:
        return None
    prices= [i['customdata'][0] for i in click['points']]
    filter=hp_data['ID'].isin(prices)
    return hp_data[filter].to_dict("records")


###Diabtes:
#Change content in selected tab:
@app.callback(
    Output('tabs-single-d', 'children'),
    Input('tabs-global-d', 'value')
)
def render_content2(tab):
    if tab == 'tab-1-d':
        return html.Div([
            checklist_diabetes,
            table_diabetes,
            dropdown_plot_diabetes,
            dropdown_vars_diabetes
        ])
        
    elif tab == 'tab-2-d':
        return None


if __name__ == '__main__':
    app.server.run(debug=True)