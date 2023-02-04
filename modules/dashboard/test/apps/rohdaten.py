import plotly.graph_objects as go
import pandas as pd

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table

# import data
kreise_df = pd.read_csv('/home/jan/Uni/DS-Project/modules/dashboard/test/assets/kreise_df.csv')
# rename and drop columns
kreise_df = kreise_df.drop(columns=['Unnamed: 0']).rename(columns={'ID_1': 'ID_Bundesland', 'NAME_1': 'Bundesland', 'ID_3': 'ID_Landkreis', 'NAME_3': 'Landkreis', 'ENGTYPE_3': 'Land_Stadt'})

# good if there are many options
Bundesland_unique = kreise_df['Bundesland'].unique()

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='Alle Landkreise auf einen Blick'), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='die wichtigsten Kennzahlen zur Filterung und zum Nachschlagen.'), className="mb-4")
        ]),
# choose between Bundesland
    dcc.Dropdown(
        id='Bundesland_choice',
        options=[
            {'label': 'Bundeland', 'value': 'Bundesland'}
        ],
        value='Bundesland',
        #multi=True,
        style={'width': '50%'}
        ),

    dbc.Row([
        dbc.Col(dash_table.DataTable(id='Rohdaten_table'),
                
                width=4)
        ])

 
])


])

# page callbacks
# display pie charts and line charts to show number of cases or deaths
@app.callback([Output('pie_cases_or_deaths', 'figure'),
               Output('line_cases_or_deaths', 'figure'),
               Output('total_pie_cases_or_deaths', 'figure'),
               Output('total_line_cases_or_deaths', 'figure')],
              [Input('cases_or_deaths', 'value')])

