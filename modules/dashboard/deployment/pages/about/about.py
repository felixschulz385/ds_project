import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/about")

content = html.Div(
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
                            width=6,
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
                            width=6,
                        ),
                    ],
                    className="mb-4",
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

layout = html.Div([content])

"""
                    Seit Sommer 2022 nutzt die Stadt Tübingen mehrere Flächen innerhalb der Auffahrtsrampen einer Bundesstraße
                    zur Erzeugung grüner Energie mittels Photovoltaik. Damit ist Tübingen deutschlandweit Vorreiter.
"""
