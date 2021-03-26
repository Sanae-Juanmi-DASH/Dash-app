
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
        data= hp_data.to_dict("records")
    )
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
    html.Div(id='tabs-content-props')
    
])




#Server:
@app.callback(
    Output('tabs-content-props', 'children'),
    Input('tabs-styled-with-props', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1'),
            table_hp
    
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])

@app.callback(
     Output('hp_table', 'data'),
     Input('data', 'children')
)

def update_table(data,tab):
        dff = pd.read_json(data)
        return dff.to_dict("records")










if __name__ == '__main__':
    app.server.run(debug=True)
