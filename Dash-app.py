
#Loading libraries:
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
import pandas as pd
import plotly.express as px
import json
import numpy as np
import plotly.graph_objects as go

#Creating app:
app = dash.Dash(__name__, title="Dash App")

#Loading dataset "House Prices":
col_names_hp=["price","lotsize","bedrooms","bathrooms","stories","driveway","recreation","fullbase","gasheat","aircon","garage","prefer"] 
hp_data= pd.read_csv('ag-data.fil', sep="\s+", names=col_names_hp)
hp_cols = [{"name": i, "id": i} for i in hp_data.columns]

#Data tyding house prices:
categ_cols_hp=["bedrooms","bathrooms","stories","driveway","recreation","fullbase","gasheat","aircon","garage","prefer"] 
for col in categ_cols_hp:
    hp_data[col]= hp_data[col].map(int)
    hp_data[col]= hp_data[col].astype(object)



#House prices table:
table_hp = html.Div([
    dt.DataTable(id="hp_table",
        columns = hp_cols,
        data= hp_data.loc[1:10,].to_dict("records")
    )
])

#House prices graphs:
hist_hp = dcc.Graph(id="hp_hist",
        figure=px.histogram(hp_data['price'], x="price")
        )


scatter_hp=dcc.Graph(id="hp_scatter",
        figure=px.scatter(hp_data['price'], x="price")
        )

boxplot_hp=dcc.Graph(id="hp_boxplot",
        figure=px.scatter(hp_data['garage'], x="garage")
        )


#Dropdown plots:
fig_names=["Histogram", "Scatter", "Boxplot"]
dropdown_plot=html.Div([
        html.Label(["Select the type of plot:",
            dcc.Dropdown(id='my-dropdown',
                options= [{'label': x, 'value': x} for x in fig_names],
                value= "Histogram",
                multi= False
            )
        ])
            
])

#User:
app.layout = html.Div([
    html.Div([
        html.H1(app.title, className= "app-header--title")]),
    dcc.Tabs(id="tabs-styled-with-props", value='tab-1', children=[
        dcc.Tab(label='House prices', value='tab-1'),
        dcc.Tab(label='2', value='tab-2'),
    ], colors={
        "border": "white",
        "primary": "Linen",
        "background": "MediumAquaMarine"
    }),
    html.Div(id='tabs-content-props'),
    html.Div(id='plot_dp')
    
])


#Server:
@app.callback(
    Output('tabs-content-props', 'children'),
    Input('tabs-styled-with-props', 'value'),    
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1'),
            table_hp,
            dropdown_plot
        ])
        
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])


#Server:
@app.callback(
    Output('plot_dp', 'children'),
    Input('my-dropdown', 'value') 
)
def render_content(dp):
    if  dp=='Scatter':
        return html.Div([
            scatter_hp
        ])
    elif dp=='Histogram':
        return html.Div([
            hist_hp
        ])
    elif dp=='Boxplot':
        return html.Div([
            boxplot_hp
        ])    
   







if __name__ == '__main__':
    app.server.run(debug=True)
