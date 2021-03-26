
#Loading libraries:
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
import pandas as pd
import plotly.express as px
import json

#Creating app:
app = dash.Dash(__name__, title="Dash App")

#Loading data:
col_names=["price","lotsize","bedrooms","bathrooms","stories","driveway","recreation"
,"fullbase","gasheat","aircon","garage","prefer"] 
housep_data= pd.read_csv('ag-data.fil', sep="\s+", names=col_names)

#User:
app.layout = html.Div([
    html.Div([
        html.H1(app.title, className= "app-header--title")]),
    dcc.Tabs(id="tabs-styled-with-props", value='tab-1', children=[
        dcc.Tab(label='House prices', value='tab-1'),
        dcc.Tab(label='2', value='tab-2'),
    ], colors={
        "border": "white",
        "primary": "Ivory",
        "background": "MediumAquaMarine"
    }),
    html.Div(id='tabs-content-props')
])




#Server:

@app.callback(
    Output('tabs-content-props', 'children'),
    Input('tabs-styled-with-props', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])












if __name__ == '__main__':
    app.server.run(debug=True)
