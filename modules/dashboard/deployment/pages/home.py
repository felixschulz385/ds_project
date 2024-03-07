import dash_bootstrap_components as dbc
import dash
from dash import Dash, Input, Output, html, dcc, callback
from dash_iconify import DashIconify
import dash_mantine_components as dmc

import pandas as pd
import geopandas as gpdx
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, path="/")

###

content = html.Div(
    [
        html.Img(
            src="assets/logo.png",
            alt="",
            style={"height": "10vh"},
            className="d-block mx-auto mb-4",
        ),
        html.H1(
            "Projekt SolarExit",
            className="fw-bold text-body-emphasis",
        ),
        dbc.Col(
            [
                html.P(
                    """
                    Entdecken Sie die Zukunft der nachhaltigen Energie! 
                    Unser wissenschaftliches Projekt untersucht das enorme Potenzial von Solaranlagen entlang von Autobahnauffahrten. Mit umweltfreundlicher Technologie und innovativen Ansätzen gestalten wir Mobilität nachhaltig. 
                    """,
                    className="mb-4 fw-light",
                ),
                dbc.Button(
                    "Zur Karte",
                    href="/karte",
                    color="primary",
                    size="lg",
                    className="px-4 me-sm-3",
                ),
            ],
            width={"size": 6},
            className="mx-auto",
        ),
    ],
    className="px-4 pt-5 text-center",
)

###
layout = html.Div([content],
                  #style={"background-image":"url('/assets/Lustnauer_Ohren_danach.jpg')",
                  #       'background-size': 'cover', 'background-repeat': 'no-repeat',
                  #       'background-position': 'center', 'height': '100vh'}
                  )
