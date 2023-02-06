import plotly.graph_objects as go
import pandas as pd
import numpy as np

from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table

from app import app

# import data
# import data
kreise_df = pd.read_csv('/home/jan/Uni/DS-Project/modules/dashboard/test/assets/kreise_df.csv')
# rename and drop columns
kreise_df = kreise_df.drop(columns=['Unnamed: 0', 'ID_1', 'ID_3']).rename(columns={'NAME_1': 'Bundesland', 'NAME_3': 'Landkreis', 'ENGTYPE_3': 'Land_Stadt'})

# good if there are many options
Bundesland_unique = kreise_df['Bundesland'].unique()
Bundesland_options = [{'label': item, 'value': item} for item in np.sort(kreise_df['Bundesland'].unique())]

# heatmap
def discrete_background_color_bins(df, n_bins=5, columns='all'):
    import colorlover
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.select_dtypes('number')
    else:
        df_numeric_columns = df[columns]
    df_max = df_numeric_columns.max().max()
    df_min = df_numeric_columns.min().min()
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
    ]
    styles = []
    legend = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        backgroundColor = colorlover.scales[str(n_bins)]['seq']['Greens'][i - 1]
        color = 'white' if i > len(bounds) / 2. else 'inherit'

        for column in df_numeric_columns:
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': color
            })
        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
                html.Div(
                    style={
                        'backgroundColor': backgroundColor,
                        'borderLeft': '1px rgb(50, 50, 50) solid',
                        'height': '10px'
                    }
                ),
                html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
            ])
        )

    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))

# run function
(styles, legend) = discrete_background_color_bins(kreise_df, columns=['avg_Score'])

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
        options=Bundesland_options,
        value=None,
        #multi=True,
        style={'width': '50%'}
        ),
# define table
    dbc.Row([
        dash_table.DataTable(
            id='table',
            # data
            columns = [{"name": i, "id": i} for i in kreise_df.columns],
            data=kreise_df.to_dict('records'),
            # sorting
            sort_action = 'native',
            sort_mode = 'multi',
            # pagination
            page_current=0,
            page_size=20,
            page_action='native',
            # style
            style_data_conditional = styles,
            style_cell_conditional=[{
                'if': {'column_id': c},
                'textAlign': 'left'
                } for c in ['Bundesland', 'Landkreis', 'Land_Stadt']],
            style_as_list_view=True,
        ),
        legend])
])])

@app.callback(
    Output('table', 'data'),
    [Input('Bundesland_choice', 'value')]
)
def update_table(Bundesland_choice):
    if Bundesland_choice:
        filtered_df = kreise_df[kreise_df['Bundesland'] == Bundesland_choice]
    else:
        filtered_df = kreise_df
    return filtered_df.to_dict(orient='records')