import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go



# import data
kreise_df = pd.read_csv('/home/jan/Uni/DS-Project/modules/dashboard/test/apps/assets/kreise_df.csv')
# rename and drop columns
kreise_df = kreise_df.drop(columns=['Unnamed: 0']).rename(columns={'NAME_1': 'Bundesland', 'NAME_2': 'Region', 'NAME_3': 'Landkreis', 'ENGTYPE_3': 'Land_Stadt'})


# create sunburst plot
Ohren_sunburst = px.sunburst(kreise_df, path=['Bundesland', 'Region', 'Landkreis'], values='avg_Score')
Ohren_sunburst = Ohren_sunburst.update_traces(
    insidetextorientation='radial',
    hovertemplate = '<b>%{label}</b> <br>Score: %{value}')


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "26rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
# the styles for the main content position it to the right of the sidebar and add some padding.
CONTENT_STYLE = {
    "margin-left": "28rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# --------------------
# SIDEBAR
# --------------------

sidebar = html.Div([
    dbc.Row([
      html.H1('Dashboard für PV-Ausbau in "Ohren"'),
      html.Hr(),
      html.P('In this research project we seek to identify the potential of photovolatic power in highway turnoffs across Germany.')
    ]),
    # Directory
    dbc.Row([
      dbc.Col([
      html.H4('Kapitel'),
        html.Ol(start=1, children=[
          html.Li([
            html.A("Einleitung", href="#einleitung"),
          ]),
          html.Li([
            html.A("Motivation", href="#motivation"),
          ]),
          html.Li([
            html.A("Aufbau", href="#aufbau"),
          ]),
          html.Li([
            html.A("Fazit", href = "#fazit"),
          ]),
          html.Li([
            html.A("Überblick Landkreise", href="#ueberblick")
          ]),
        ])])]),
    dcc.Markdown('''
        | Mitwirkende | Matrikelnummer |
        | ---         | ---:           |
        |Yvette Brody | 1234 |
        |Marvin Hoberg| 1234 |
        |Felix Schulz | 1234 |
        |Jan Besler   |5629079|
    '''),
    # Links und Erklärungen
    dbc.Row([
      dbc.Col(["GitHub Repo",
        DashIconify(icon="bi:github"),
        #href="https://github.com/felixschulz385/ds_project",
      ]),
      dbc.Col(["How it started",
        DashIconify(icon="bi:newspaper"),
        #href="https://www.badische-zeitung.de/ob-palmer-will-solaranlagen-auf-freien-stellen-neben-bundesstrassen--211487616.html",
      ]),
      html.Hr(),
      html.P('This project is being developed as part of the \
              Data Science in Business and Economics Master degree course at the University of Tübingen.')
    ])
], style=SIDEBAR_STYLE)

# --------------------
# MAIN PAGE
# --------------------

# images
import base64
with open("/home/jan/Uni/DS-Project/modules/dashboard/test/apps/assets/economic_model.jpeg", "rb") as file:
    economic_model_img = "data:image/jpg;base64, {}".format(base64.b64encode(file.read()).decode("utf-8"))
with open("/home/jan/Uni/DS-Project/modules/dashboard/test/apps/assets/brandenburg_driveways.jpg", "rb") as file:
    BB_ohren = "data:image/jpg;base64, {}".format(base64.b64encode(file.read()).decode("utf-8"))
# carousel pictures
with open("/home/jan/Uni/DS-Project/modules/dashboard/test/apps/assets/lustnauer_ohren.jpg", "rb") as file:
    carousel_1 = "data:image/jpg;base64, {}".format(base64.b64encode(file.read()).decode("utf-8"))
with open("/home/jan/Uni/DS-Project/modules/dashboard/test/apps/assets/driveways_example_6.jpg", "rb") as file:
    carousel_2 = "data:image/jpg;base64, {}".format(base64.b64encode(file.read()).decode("utf-8"))
with open("/home/jan/Uni/DS-Project/modules/dashboard/test/apps/assets/driveways_example_7.jpg", "rb") as file:
    carousel_3 = "data:image/jpg;base64, {}".format(base64.b64encode(file.read()).decode("utf-8"))
    
content = html.Div([
    dbc.Container([
        # Überschriften & Einleitung
        dbc.Row([
            dbc.Col(html.H1("Lustnauer 'Ohren' skaliert auf ganz Deutschland", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='Erkennen von ungenutzten Potenzialen in ungenutzten Flächen.'
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children='Auf der zweiten Seite wird eine interaktive Karte dargestellt, welche die verschiedenen Ohren ranked'
                                     'Die dritte Seite präsentiert dieselben Daten in tabellarischer Form, zum erkunden und nachschlagen.')
                    , className="mb-5")
        ]),


        # Einleitung
        dbc.Row([
            html.Hr(),
            html.H3('Einleitung', id="einleitung")
        ], class_name='mt-2'),
        dbc.Row([
            dcc.Markdown('''
                bla bla bla
            ''')
        ]),
        dbc.Row([
            dbc.Carousel(
                items=[
                    {"key": "1",
                    "src": carousel_1,
                    "header": "Beispiel Ohren",
                    "caption": "",},
                    {"key": "2",
                    "src": carousel_2,
                    "header": "ausgeschnittene Flächen",
                    "caption": "",},
                    {"key": "3",
                    "src": carousel_3,
                    "header": "zusammengesetztes Bild",
                    "caption": "",},
            ], style = {
                'width': '80vh',
                'height': '80vh',
                'padding': '10vh 5vh'
                })
        ]),
        
        # Motivation
        dbc.Row([
            html.Hr(),
            html.H3('Motivation', id="motivation")
        ], class_name='mt-2'),
        dbc.Row([
            dcc.Markdown('''
                Global climate change has put Germany's energy industry in a state of turmoil. 
                After years of heavy relicance on coal and gas (in 2010, 25% of the German Energy Mix 
                were sourced this way ([BDEW, 2022](https://www.bdew.de/energie/bruttostromerzeugung-seit-2010/))), 
                climate pledges have forced leaders to steer away towards renewables 
                ([Bundesregierung, 2022](https://www.bundesregierung.de/breg-en/issues/climate-action/government-climate-policy-1779414)). 

                While contruction of onshore wind parks is repeatedly halted by local opposition ([DW, 2022](https://p.dw.com/p/4K361)),
                installed photovoltaic (PV) capacity has steadily and rapidly grown in the recent years
                ([Bundesnetzagentur, 2022](https://www.smard.de/home/marktdaten)). One of its great benefits is the much lower footprint
                of the panels compared to wind parks. This allows PV to be installed in places with little other use, 
                most prominently on house roofs. Several German states have in fact made PV mandatory on new buildings 
                ([Imolauer, 2022](https://www.roedl.com/insights/renewable-energy/2021/august/pv-obligation-germany-federal-states)). 

                Looking for further opportunities, the southern-German city of Tübingen found the space inside one of their highway ramps
                to be highly suited for PV use
                ([swt, 2022](https://www.swtue.de/energie/strom/erneuerbare-energien/bautagebuecher/solarpark-lustnauer-ohren.html)).
                After several years of legal hassle, the site is now the city's largest source of green energy.

                Its great benefit - similar to house roofs - is that there is little alternative use cases for the area.
                Encircled by traffic and pollution, the city and us authors believe that PV energy production is an ingenious idea
                to repurpose these human-made wastelands. Germany features a large network of divided laneways in its
                Autobahn and Bundesstraße road systems. The many connections to local roads may serve as excellent opportunities
                for PV energy production in the future.
            '''),
            dbc.Card([
                dbc.CardImg(src = BB_ohren, top=True),
                dbc.CardBody(
                    html.P("Beispielbild der potenziellen Flächen.", className="card-text")),
            ],style={"height": "70vh", "width": "70vh"},)

        ]),
        
        # Aufbau
        dbc.Row([
            html.Hr(),
            html.H3('Aufbau', id="aufbau")
        ], class_name='mt-2'),
        dbc.Row([
            dcc.Markdown('''
                Our project seeks to provide a comprehensive overview on the potential in equiping highway turnoffs across Germany with photovoltaics.
                Using state-of-the-art GIS software and Machine Learning techniques we identify turnoffs and evaluate their suitability.
                Beginning with a limited scope on the German state of Brandenburg, we plan to extend our models to cover the entire nation's road network.

                Core elements of the research project include:
                    - [x] Identification of highway turnoffs
                    - [ ] Evaluation of existing build-up and vegetation using satellite imagery and a Deep Neural Network
                    - [ ] Further economic considerations
                        - [ ] Proximity to power grid
                        - [ ] Terrain suitability
                        - [ ] Macro-level wheather considerations based on sunlight
                        - [ ] Optimal angle of construction and safety of passing cars
                    - [ ] Presentation of findings in a Dashboard

                Economic suitability of a potential spot is measured with the following economic model:
            '''),
            dbc.Card([
                html.Img(src = economic_model_img),
                dbc.CardBody(
                    html.P("Structure of the economic model.", className="card-text")),
            ],style={"height": "70vh", "width": "70vh"},)
        ]),
        
        # Sunburst Plot
        dbc.Row([
            html.Hr(),
            html.H3('Überblick Landkreise', id = "ueberblick")
        ], class_name='mt_2'),
        # Sunburst Plot
        dbc.Row([dbc.Col([
            dcc.Graph(figure = Ohren_sunburst, responsive=True, style = {'height': '100vh', 'width': '100vh'})
            ], class_name = "d-flex justify-content-center")
        ])

    ])

], style=CONTENT_STYLE)

layout = html.Div([sidebar, content])