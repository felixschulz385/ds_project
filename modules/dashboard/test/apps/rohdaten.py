import plotly.graph_objects as go
import pandas as pd
import numpy as np

from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from app import app, path_directory
# --------------
# import data
# --------------
# kreise
kreise_df = pd.read_csv(path_directory + 'apps/assets/kreise_df.csv')
# rename and drop columns
kreise_df = kreise_df.drop(columns=['Unnamed: 0']).rename(columns={
    'NAME_1': 'Bundesland',
    'NAME_2': 'Landkreis',
    'terrain_score': 'Geländebeschaffenheit',
    'irridation_score': 'Sonnenpotential',
    'distance_score': 'Netzanschluss',
    'overall_score': 'Gesamtwertung'
    })
# Reorder the columns
column_order = ['Landkreis', 'Bundesland', 'Geländebeschaffenheit', 'Sonnenpotential', 'Netzanschluss', 'Gesamtwertung']
kreise_df = kreise_df.reindex(columns=column_order)

# gemeinde
gemeinde_df = pd.read_csv(path_directory + 'apps/assets/gemeinde_df.csv')
# rename and drop columns
gemeinde_df = gemeinde_df.drop(columns=['Unnamed: 0.1', 'Unnamed: 0', 'suitable_area']).rename(columns={
    'NAME_1': 'Bundesland',
    'NAME_2': 'Landkreis',
    'NAME_3': 'Gemeinde',
    'terrain_score': 'Geländebeschaffenheit',
    'irridation_score': 'Sonnenpotential',
    'distance_score': 'Netzanschluss',
    'overall_score': 'Gesamtwertung'
    })
# Reorder the columns
column_order = ['Gemeinde', 'Landkreis', 'Bundesland', 'Geländebeschaffenheit', 'Sonnenpotential', 'Netzanschluss', 'Gesamtwertung']
gemeinde_df = gemeinde_df.reindex(columns=column_order)

# good if there are many options
Bundesland_unique = kreise_df['Bundesland'].unique()
Bundesland_options = [{'label': item, 'value': item} for item in np.sort(kreise_df['Bundesland'].unique())]
Kreise_unique = kreise_df['Landkreis'].unique()
Kreise_options = [{'label': item, 'value': item} for item in np.sort(kreise_df['Landkreis'].unique())]


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
(styles_kreise, legend_kreise) = discrete_background_color_bins(kreise_df, columns=['Gesamtwertung'])
(styles_gemeinde, legend_gemeinde) = discrete_background_color_bins(gemeinde_df, columns=['Gesamtwertung'])

# --------------------
# MAIN PAGE
# --------------------
layout = html.Div([
    dbc.Row([
            dbc.Col(html.H1(children='Alle Landkreise auf einen Blick'), className="mb-1")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='die wichtigsten Kennzahlen zur Filterung und zum Nachschlagen.'), className="mb-3")
        ]),
    # tabs for Kreis & Gemeinde
    dmc.Tabs([
        dmc.TabsList([
            dmc.Tab("Gemeinden", value = "gemeinde"),
            dmc.Tab("Landkreise", value = "kreise"),
        ], grow=False),
        dmc.TabsPanel(
            dbc.Container([
                # dropdown menu
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(
                            id='Bundesland_g_choice',
                            options=Bundesland_options,
                            value=None,
                            placeholder="Bundesland",
                            style={'width': '30vh'}),
                    ]),
                    dbc.Col([
                        dcc.Dropdown(
                            id='Landkreis_choice',
                            options=Kreise_options,
                            value=None,
                            placeholder="Landkreis",
                            style={'width': '30vh'}),
                    ]),
                ], className="mb-2 mt-4"),
                # table
                dbc.Row([
                    dash_table.DataTable(
                        id='table_g',
                        # data
                        columns = [{"name": i, "id": i} for i in gemeinde_df.columns],
                        data=gemeinde_df.to_dict('records'),
                        # sorting
                        sort_action = 'native',
                        sort_mode = 'multi',
                        # pagination
                        page_current=0,
                        page_size=25,
                        page_action='native',
                        # style
                        style_data_conditional = styles_gemeinde,
                        style_cell_conditional=[{
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in ['Bundesland', 'Landkreis', 'Gemeinde']],
                        style_as_list_view=True,
                    ), legend_gemeinde],
                        #style={'margin-left': '10vh','margin-right': '10vh'}
                        )
            ]), value = "gemeinde"
        ),
        dmc.TabsPanel(
            dbc.Container([
                # dropdown menu
                dbc.Row([
                    dcc.Dropdown(
                        id='Bundesland_k_choice',
                        options=Bundesland_options,
                        value=None,
                        placeholder="Bundesland",
                        style={'width': '30vh'}
                    ),
                ], className="mb-2 mt-4"),
                # table
                dbc.Row([
                    dash_table.DataTable(
                        id='table_k',
                        # data
                        columns = [{"name": i, "id": i} for i in kreise_df.columns],
                        data=kreise_df.to_dict('records'),
                        # sorting
                        sort_action = 'native',
                        sort_mode = 'multi',
                        # pagination
                        page_current=0,
                        page_size=25,
                        page_action='native',
                        # style
                        style_data_conditional = styles_kreise,
                        style_cell_conditional=[{
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in ['Bundesland', 'Landkreis']],
                        style_as_list_view=True,
                    ), legend_kreise],
                        #style={'margin-left': '10vh','margin-right': '10vh'}
                        )
            ]), value = "kreise"
        ),
    ],
    color = "yellow",
    orientation = "horizontal",
    value = "gemeinde"),
        
], style={'margin-right': '2rem',
          'margin-left': '2rem'})

# kreise callbacks

@app.callback(
    Output('table_k', 'data'),
    [Input('Bundesland_k_choice', 'value')]
)
def update_table(Bundesland_k_choice):
    if Bundesland_k_choice:
        filtered_df = kreise_df[kreise_df['Bundesland'] == Bundesland_k_choice]
    else:
        filtered_df = kreise_df
    return filtered_df.to_dict(orient='records')

# gemeinde callbacks

@app.callback(
    Output('table_g', 'data'),
    [Input('Bundesland_g_choice', 'value'),
     Input('Landkreis_choice', 'value')]
)

def update_table(Bundesland_g_choice, Landkreis_choice):
    if Bundesland_g_choice is None and Landkreis_choice is None:
        return gemeinde_df.to_dict(orient='records')
    if Bundesland_g_choice is not None and Landkreis_choice is not None:
        filtered_df = gemeinde_df[(gemeinde_df['Bundesland'] ==Bundesland_g_choice) & (gemeinde_df['Landkreis'] == Landkreis_choice)]
        return filtered_df.to_dict(orient='records')
    if Bundesland_g_choice is not None:
        filtered_df = gemeinde_df[gemeinde_df['Bundesland'] ==Bundesland_g_choice]
        return filtered_df.to_dict(orient='records')
    if Landkreis_choice is not None:
        filtered_df = gemeinde_df[gemeinde_df['Landkreis'] == Landkreis_choice]
        return filtered_df.to_dict(orient='records')
