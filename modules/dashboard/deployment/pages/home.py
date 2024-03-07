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

top_element = html.Div(
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
                    Unser wissenschaftliches Projekt untersucht das enorme Potenzial von Solaranlagen entlang von Autobahnauffahrten.
                    """,
                    className="mb-4 fw-light",
                ),
                dbc.Button(
                    "Zur Karte",
                    href="/karte",
                    color="primary",
                    size="lg",
                    className="mb-4 px-4 me-sm-3",
                ),
            ],
            md = {"size": 6}, xs = {"size": 12},
            className="mx-auto",
        ),
    ],
    className="px-4 pt-5 text-center my-5",
)

bottom_element = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.H2("Das Projekt"),
                                        html.P(
                                            "Das Erreichen der deutschen Ziele in der Energiewende verlangt innovative Ansätze",
                                            className="fs-6",
                                        ),
                                        dbc.Button(
                                            "Mehr Erfahren",
                                            href="/about/projekt",
                                            className="btn-primary",
                                        ),
                                    ],
                                    className="h-100 p-5 bg-light rounded-3",
                                )
                            ],
                            md = {"size": 6}, xs = {"size": 12},
                            className = " mb-4",
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.H2("Das Team"),
                                        html.P(
                                            "Diese Webseite enstand im Rahmen eines Projektseminars an der Universität Tübingen",
                                            className="fs-6",
                                        ),
                                        dbc.Button(
                                            "Mehr Erfahren",
                                            href="/about/team",
                                            className="btn-primary",
                                        ),
                                    ],
                                    className="h-100 p-5 bg-light rounded-3",
                                )
                            ],
                            md = {"size": 6}, xs = {"size": 12},
                            className = " mb-4",
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.H1(
                                            "Wie es funktioniert",
                                            className="display-5 fw-bold",
                                        ),
                                        html.P(
                                            "Unsere Auswertung entstand unter Verwendung modernster Technologien der künstlichen Intelligenz",
                                            className="fs-6",
                                        ),
                                        dbc.Button(
                                            "Mehr Erfahren",
                                            href="/about/technologie",
                                            className="btn-primary",
                                        ),
                                    ],
                                    className="h-100 p-5 bg-dark text-white rounded-3",
                                ),
                            ],
                            width={"size": 12},
                        )
                    ],
                    className="mb-4",
                ),
            ],
            className="py-4",
        )
    ]
)

###
layout = html.Div([top_element, bottom_element],
                  #style={"background-image":"url('/assets/Lustnauer_Ohren_danach.jpg')",
                  #       'background-size': 'cover', 'background-repeat': 'no-repeat',
                  #       'background-position': 'center', 'height': '100vh'}
                  )
